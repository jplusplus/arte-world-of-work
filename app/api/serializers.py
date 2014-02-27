from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.serializers import ValidationError

from app.core import mixins as core_mixins 
from app.core.models import *
from app.api import mixins


class ResultsSerializer(serializers.Serializer):
    def to_native(self, value):
        return value.as_dict()

class QuestionMediaSerializer(serializers.ModelSerializer):
    picture = serializers.SerializerMethodField('get_picture')
    class Meta:
        model = QuestionMediaAttachement
        exclude = ('question',)

    def get_picture(self, obj):
        return obj.picture.url if obj.picture else None

class MediaChoiceFieldSerializer(QuestionMediaSerializer):
    class Meta:
        model = MediaChoiceField

class UserChoiceFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChoiceField
        fields = ('value',)


class ChoiceField(mixins.GenericModelMixin):
    ctype_mapping = {
        MediaChoiceField: MediaChoiceFieldSerializer,
        UserChoiceField: UserChoiceFieldSerializer
    }

    class Meta:
        model = BaseChoiceField
        exclude = ('question', )

class StaticFeedbackSerializer(serializers.ModelSerializer):
    picture = serializers.SerializerMethodField('get_picture')
    class Meta:
        model = StaticFeedback
    def get_picture(self, obj):
        return obj.picture.url if obj.picture else None

class FeedbackSerializer(mixins.InheritedModelMixin):
    model_mapping = {
        StaticFeedback: StaticFeedbackSerializer
    }

    sub_type = serializers.Field()
    class Meta:
        model = BaseFeedback
        fields = ('html_sentence', 'sub_type')


class MultipleChoicesSerializer(serializers.ModelSerializer):
    choices    = ChoiceField(source='basechoicefield_set', many=True)    
    has_medias = serializers.Field(source='has_medias')

    class Meta:
        model = BaseQuestion

    def to_native(self, value): 
        base_data = super(MultipleChoicesSerializer, self).to_native(value)
        if isinstance(value, core_mixins.ValidateButtonMixin):
            base_data['validate_button_label'] = value.validate_button_label
        if isinstance(value, core_mixins.MediaTypeMixin):            
            base_data['media_type'] = value.media_type
        return base_data

class TypedNumberQuestionSerializer(serializers.ModelSerializer):
    class Meta: 
        model = TypedNumberQuestion

class BooleanQuestionSerializer(MultipleChoicesSerializer):
    class Meta: 
        model = BooleanQuestion

class UserAgeQuestionSerializer(serializers.ModelSerializer): 
    class Meta: model = UserAgeQuestion

class UserCountryQuestionSerializer(serializers.ModelSerializer):
    class Meta: model = UserCountryQuestion

question_mapping = {
    UserAgeQuestion:         UserAgeQuestionSerializer,
    UserCountryQuestion:     UserCountryQuestionSerializer,
    BooleanQuestion:         BooleanQuestionSerializer,
    TypedNumberQuestion:     TypedNumberQuestionSerializer,
    UserGenderQuestion:      MultipleChoicesSerializer,
    TextSelectionQuestion:   MultipleChoicesSerializer,
    TextRadioQuestion:       MultipleChoicesSerializer,
    MediaRadioQuestion:      MultipleChoicesSerializer,
    MediaSelectionQuestion:  MultipleChoicesSerializer,
}

class QuestionSerializer(mixins.InheritedModelMixin):
    model_mapping = question_mapping 
    # we have to explicitly declare this field because it's a model property
    typology = serializers.Field()
    media    = QuestionMediaSerializer(source='questionmediaattachement')
    class Meta:
        model = BaseQuestion
        # fields = ('id', 'label', 'skip_button_label', 'typology')
        depth = 1
        exclude = ('content_type',)


class QuestionResultsSerializer(mixins.InheritedModelMixin):
    model_mapping = question_mapping 
    typology = serializers.Field()
    results  = serializers.SerializerMethodField('get_results')
    class Meta:
        model  = BaseQuestion
        exclude = ('content_type',)
        depth  = 1


    def get_results(self, question):
        request = self.context['request']
        params  = request.QUERY_PARAMS
        filters = {}
        filters['age_min'] = params.get('age_min', None)
        filters['age_max'] = params.get('age_max', None)
        filters['gender']  = params.get('gender', None)
        if not issubclass(question.content_type.model_class(), UserProfileQuestion):
            serializer = ResultsSerializer(question.results(**filters)) 
            return serializer.data
        return None


# -----------------------------------------------------------------------------
# 
#   Generic thematic elements
#
# -----------------------------------------------------------------------------
class ThematicElementSerializer(mixins.GenericModelMixin):
    type = serializers.Field()
    ctype_mapping = {
        BaseFeedback: FeedbackSerializer,
        BaseQuestion: QuestionSerializer
    }

    class Meta:
        model = ThematicElement
        field = ('position', 'type')
        exclude = ('content_type','id')
        depth = 0

class ThematicElementResultsSerializer(ThematicElementSerializer):
    # same as ThematicElementSerializer but instead of using a QuestionSerializer
    # we use a QuestionResultsSerializer 
    ctype_mapping = {
        BaseFeedback: FeedbackSerializer,
        BaseQuestion: QuestionResultsSerializer 
    }

# -----------------------------------------------------------------------------
# 
#   Thematic
#
# -----------------------------------------------------------------------------
class ThematicSerializer(serializers.ModelSerializer):
    elements = serializers.PrimaryKeyRelatedField(many=True, source='thematicelement_set')
    class Meta:
        model = Thematic
        fields = ('id', 'title',  'intro_description', 'intro_button_label', 
            'elements', 'position', 'slug')
        depth = 1

class NestedThematicSerializer(ThematicSerializer):
    elements = ThematicElementSerializer(many=True, source='thematicelement_set')

class ThematicResultsSerializer(ThematicSerializer):
    elements = ThematicElementResultsSerializer(many=True, source='thematicelement_set')


# -----------------------------------------------------------------------------
#
#  User related serializers (+ auth ?)
#
# -----------------------------------------------------------------------------

class UserSerializer(serializers.ModelSerializer):
    profile = serializers.RelatedField(source='userprofile', many=False)
    token   = serializers.SerializerMethodField('get_token')
    class Meta:
        model = get_user_model()

    def get_token(self, user):
        return Token.objects.get(user=user)

class UserPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPosition


# -----------------------------------------------------------------------------
#
# Answer serializers 
#
# -----------------------------------------------------------------------------
class RadioSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = RadioAnswer        
        exclude = ('content_type',)

    def validate_value(self, attrs, source):
        value = attrs.get('value')
        question = attrs.get('question').as_final()

        out_of_choices = question.choices().filter(id=value.pk).count() == 0

        if value == None:
            raise ValidationError(_('You have to select at least one choice'))
        elif out_of_choices:
            raise ValidationError(_('This choice {c} is not related to the answered question').format(c=choice))
        return attrs

class SelectionSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = SelectionAnswer
        exclude = ('content_type',)

    def validate_value(self, attrs, source):
        value = attrs.get('value')
        question = attrs.get('question').as_final()
        if len(value) > 0:
            for choice in value:
                if choice.question.pk != question.pk:
                    raise ValidationError(_('This choice {c} is not related to the answered question').format(c=choice))
        else:
            raise ValidationError(_('You have to select at least one choice'))
        return attrs

class TypedNumberSerializer(serializers.ModelSerializer):
    class Meta: 
        model = TypedNumberAnswer
        exclude = ('content_type',)

class UserAgeSerializer(serializers.ModelSerializer):
    class Meta: 
        model = UserAgeAnswer
        exclude = ('content_type',)

class UserCountrySerializer(serializers.ModelSerializer):
    class Meta: 
        model = UserCountryAnswer
        exclude = ('content_type',)

class UserGenderSerializer(serializers.ModelSerializer):
    class Meta: 
        model = UserGenderAnswer
        exclude = ('content_type',)

class AnswerSerializer(mixins.InheritedModelMixin):
    class Meta:
        model = BaseAnswer

    model_mapping = {
        BooleanAnswer:     RadioSerializer,
        RadioAnswer:       RadioSerializer,
        SelectionAnswer:   SelectionSerializer,
        TypedNumberAnswer: TypedNumberSerializer,
        UserAgeAnswer:     UserAgeSerializer, 
        UserGenderAnswer:  UserGenderSerializer, 
        UserCountryAnswer: UserCountrySerializer, 
    }

    def as_final_serializer(self, data, files):
        final_question = BaseQuestion.objects.get_final_question(pk=data.get('question'))
        serializer     = self.get_final_serializer(final_question.answer_type())
        return serializer(data=data, files=files)

class CountrySerializer(serializers.Serializer):
    iso_code = serializers.CharField(max_length=2)
    name = serializers.CharField(max_length=120)

    def to_native(self, value):
        return {
            'iso_code': value[0],
            'name': unicode(value[1])
        }



