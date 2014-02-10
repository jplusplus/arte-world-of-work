from rest_framework import serializers
from app.core.models import *
from django.contrib.auth import get_user_model
from six import with_metaclass

class ThematicElementField(serializers.RelatedField):
    type = serializers.Field()
    class Meta:
        model = ThematicElement
        field = ('position', 'type')
        depth = 0

    def to_native(self, value):
        rel_klass  = value.content_type.model_class()
        if issubclass(rel_klass, BaseFeedback):
            serializer = FeedbackSerializer(value.content_object)
        elif issubclass(rel_klass, BaseQuestion):
            serializer = QuestionSerializer(value.content_object)

        base_data  = ThematicElementSerializer(value).data
        base_data.update({ 'type': value.type })
        base_data.update(serializer.data)
        return base_data

class ThematicElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThematicElement
        exclude = ('content_type','id')


class ChoiceField(serializers.ModelSerializer):
    class Meta:
        model = BaseChoiceField
    def to_native(self, value):
        return super(ChoiceField, self).to_native(value)

class FeedbackSerializer(serializers.ModelSerializer):
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
            serializer = StaticFeedbackSerializer(value)
        return serializer

class StaticFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticFeedback

class QuestionSerializer(serializers.ModelSerializer):
    typology = serializers.Field()
    class Meta:
        model = BaseQuestion
        fields = ('id', 'label', 'skip_button_label', 'typology')
        depth = 1

    def to_native(self, value):
        base_data = super(QuestionSerializer, self).to_native(value)
        serializer = self.get_final_serializer(value)
        if serializer:
            base_data.update(serializer.data)
        return base_data

    def get_final_serializer(self, value):
        serializer = None
        if isinstance(value, UserAgeQuestion):
            serializer = UserAgeQuestionSerializer(value)
        elif isinstance(value, BooleanQuestion):
            serializer = BooleanQuestionSerializer(value)
        elif isinstance(value, TypedNumberQuestion):
            serializer = TypedNumberQuestionSerializer(value)
        return serializer

class MultipleChoicesSerializer(serializers.ModelSerializer):
    choices = ChoiceField(source='basechoicefield_set', many=True)

class TypedNumberQuestionSerializer(serializers.ModelSerializer):
    class Meta: 
        model = TypedNumberQuestion
        fields = ('unit', 'min_number', 'max_number',)

class BooleanQuestionSerializer(MultipleChoicesSerializer):
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
    elements = ThematicElementField(many=True, source='thematicelement_set')

class UserSerializer(serializers.ModelSerializer):
    profile = serializers.RelatedField(source='userprofile', many=False)
    class Meta:
        model = get_user_model()


class UserPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPosition

