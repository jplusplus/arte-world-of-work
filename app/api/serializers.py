from rest_framework import serializers
from app.core.models import *
from django.contrib.auth import get_user_model

class InherithedModelSerializerMixin(object):
    def as_final_serializer(self, data, files):
        raise NotImplementedError('Please implement this method on your serializer')

class ThematicElementSerializer(serializers.ModelSerializer):
    type = serializers.Field()
    class Meta:
        model = ThematicElement
        field = ('position', 'type')
        exclude = ('content_type','id')
        depth = 0

    def to_native(self, value):
        base_data  = super(ThematicElementSerializer, self).to_native(value)
        rel_klass  = value.content_type.model_class()
        if issubclass(rel_klass, BaseFeedback):
            serializer = FeedbackSerializer(value.content_object)
        elif issubclass(rel_klass, BaseQuestion):
            serializer = QuestionSerializer(value.content_object)
        base_data.update(serializer.data)
        return base_data

class ChoiceField(serializers.ModelSerializer):
    class MediaChoiceFieldSerializer(serializers.ModelSerializer):
        class Meta:
            model = MediaChoiceField
            fields = ('picture',)

    class Meta:
        model = BaseChoiceField
        exclude = ('question', )

    def to_native(self, value):
        base_data = super(ChoiceField, self).to_native(value)
        # check if this choice field 
        if isinstance(value.content_object, MediaChoiceField):
            final_data = ChoiceField.MediaChoiceFieldSerializer(value.content_object).data
            base_data.update(final_data)
        return base_data

class FeedbackSerializer(serializers.ModelSerializer):
    class StaticFeedbackSerializer(serializers.ModelSerializer):
        class Meta:
            model = StaticFeedback

    sub_type = serializers.Field()
    class Meta:
        model = BaseFeedback
        fields = ('html_sentence', 'sub_type')

    def to_native(self, value):
        base_data  = super(FeedbackSerializer, self).to_native(value)
        base_data.update({'': value.sub_type})
        serializer = self.get_final_serializer(value)
        if serializer:
            base_data.update(serializer.data)
        return base_data

    def get_final_serializer(self, value):
        serializer = None
        if isinstance(value, StaticFeedback):
            serializer = FeedbackSerializer.StaticFeedbackSerializer(value)
        return serializer


class QuestionSerializer(serializers.ModelSerializer):
    typology = serializers.Field()
    class Meta:
        model = BaseQuestion
        # fields = ('id', 'label', 'skip_button_label', 'typology')
        depth = 1
        exclude = ('content_type',)

    def to_native(self, value):
        base_data = super(QuestionSerializer, self).to_native(value)
        serializer = self.get_final_serializer(value)
        if serializer:
            base_data.update(serializer.data)
        return base_data

    def get_final_serializer(self, value):
        serializer = None
        klass = value.__class__
        if isinstance(value, UserAgeQuestion):
            serializer = UserAgeQuestionSerializer(value)
        elif isinstance(value, BooleanQuestion):
            serializer = BooleanQuestionSerializer(value)
        elif isinstance(value, TypedNumberQuestion):
            serializer = TypedNumberQuestionSerializer(value)
        elif isinstance(value, UserGenderQuestion) \
            or issubclass(klass, RadioQuestionMixin) \
            or issubclass(klass, SelectionQuestionMixin):
            serializer = MultipleChoicesSerializer(value)
        return serializer

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
    class Meta(MultipleChoicesSerializer.Meta): 
        model = BooleanQuestion

class UserAgeQuestionSerializer(serializers.ModelSerializer):
    class Meta(QuestionSerializer.Meta):
        model = UserAgeQuestion

class ThematicSerializer(serializers.ModelSerializer):
    elements = serializers.PrimaryKeyRelatedField(many=True, source='thematicelement_set')
    class Meta:
        model = Thematic
        fields = ('id', 'title',  'intro_description', 
            'intro_button_label', 'elements')
        depth = 1

class NestedThematicSerializer(ThematicSerializer):
    elements = ThematicElementSerializer(many=True, source='thematicelement_set')

class UserSerializer(serializers.ModelSerializer):
    profile = serializers.RelatedField(source='userprofile', many=False)
    class Meta:
        model = get_user_model()


class UserPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPosition


class AnswerSerializer(serializers.Serializer, InherithedModelSerializerMixin):
    def as_final_serializer(self, data, files):
        final_question = BaseQuestion.objects.get_final_question(pk=data.get('question'))
        return self.get_final_serializer(final_question.answer_type)(data=data, files=files)

    def to_native(self, value):
        base_data = super(AnswerSerializer, self).to_native(value)
        final_serializer = self.get_final_serializer(value.content_type.model_class())
        if final_serializer != None:
            base_data.update(final_serializer(value.content_object).data)
        return base_data
        
    def get_final_serializer(self, klass):
        klass_to_serializer = {
            TypedNumberAnswer: TypedNumberSerializer,
            SelectionAnswer: SelectionSerializer,
            RadioAnswer: RadioSerializer,
        }
        return klass_to_serializer[klass]


class RadioSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = RadioAnswer        

class TypedNumberSerializer(serializers.ModelSerializer):
    class Meta: 
        model = TypedNumberAnswer
        exclude = ('content_type',)

class SelectionSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = SelectionAnswer