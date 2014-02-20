from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from app.core.models import *
from app.api import mixins


class ResultsSerializer(serializers.Serializer):
    def to_native(self, value):
        return value.as_dict()

class MediaChoiceFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaChoiceField
        fields = ('picture',)

class ChoiceField(mixins.GenericModelMixin):
    ctype_mapping = {
        MediaChoiceField: MediaChoiceFieldSerializer
    }

    class Meta:
        model = BaseChoiceField
        exclude = ('question', )

class StaticFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticFeedback

class FeedbackSerializer(mixins.InheritedModelMixin):
    model_mapping = {
        StaticFeedback: StaticFeedbackSerializer
    }

    sub_type = serializers.Field()
    class Meta:
        model = BaseFeedback
        fields = ('html_sentence', 'sub_type')


class MultipleChoicesSerializer(serializers.ModelSerializer):
    choices = ChoiceField(source='basechoicefield_set', many=True)
    class Meta:
        model = BaseQuestion

    def to_native(self, value): 
        base_data = super(MultipleChoicesSerializer, self).to_native(value)
        if isinstance(value, ValidateButtonMixin):
            base_data['validate_button_label'] = value.validate_button_label
        return base_data

class TypedNumberQuestionSerializer(serializers.ModelSerializer):
    class Meta: 
        model = TypedNumberQuestion

class BooleanQuestionSerializer(MultipleChoicesSerializer):
    choices = ChoiceField(source='basechoicefield_set', many=True)
    class Meta: 
        model = BooleanQuestion

class UserAgeQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAgeQuestion

question_mapping = {
    UserAgeQuestion:         UserAgeQuestionSerializer,
    BooleanQuestion:         BooleanQuestionSerializer,
    TypedNumberQuestion:     TypedNumberQuestionSerializer,
    UserGenderQuestion:      MultipleChoicesSerializer,
    RadioQuestionMixin:      MultipleChoicesSerializer,
    SelectionQuestionMixin:  MultipleChoicesSerializer
}

class QuestionSerializer(mixins.InheritedModelMixin):
    model_mapping = question_mapping 
    # we have to explicitly declare this field because it's a model property
    typology = serializers.Field() 
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
        serializer = ResultsSerializer(question.results(**filters)) 
        return serializer.data



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

class UserSerializer(serializers.ModelSerializer):
    profile = serializers.RelatedField(source='userprofile', many=False)
    class Meta:
        model = get_user_model()

class UserPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPosition

class RadioSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = RadioAnswer        
        exclude = ('content_type',)

class TypedNumberSerializer(serializers.ModelSerializer):
    class Meta: 
        model = TypedNumberAnswer
        exclude = ('content_type',)

class SelectionSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = SelectionAnswer
        exclude = ('content_type',)

    def validate_value(self, attrs, source):
        # super(SelectionSerializer, self).validate(attrs)
        value = attrs.get('value')
        question = attrs.get('question').as_final()
        if len(value) > 0:
            for choice in value:
                if choice.question.pk != question.pk:
                    raise ValidationError(_('This choice {c} is not related to the answered question').format(c=choice))
        else:
            raise ValidationError(_('You have to select at least one choice'))
        return attrs

class AnswerSerializer(mixins.InheritedModelMixin):
    class Meta:
        model = BaseAnswer

    model_mapping = {
        TypedNumberAnswer: TypedNumberSerializer,
        SelectionAnswer: SelectionSerializer,
        RadioAnswer: RadioSerializer,
    }

    def as_final_serializer(self, data, files):
        final_question = BaseQuestion.objects.get_final_question(pk=data.get('question'))
        return self.get_final_serializer(final_question.answer_type())(data=data, files=files)

