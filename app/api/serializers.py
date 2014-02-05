from rest_framework import serializers
from app.core.models import *


class ThematicElementField(serializers.RelatedField):
    class Meta:
        model = ThematicElement

    def to_native(self, value): 
        serializer = None
        # import pdb; pdb.set_trace()
        rel_object = value.content_object
        if isinstance(rel_object, BaseFeedback):
            serializer = FeedbackSerializer(rel_object)
        if isinstance(rel_object, BaseQuestion):
            serializer = QuestionSerializer(rel_object)
        serializer.data['position'] = value.position
        return serializer.data

class ChoiceField(serializers.RelatedField):
    def to_native(self, value):
        pass


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseFeedback

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseQuestion
        fields = ('id', 'label', 'skip_button_label')
        depth = 1

    def to_native(self, value):
        serializer = self.get_final_serializer(value)
        if serializer is None:
            data = super(QuestionSerializer, self).to_native(value)
        else:
            data = serializer.data
        data['typology'] = value.content_type.model_class().__name__
        data['answer_type'] = value.answer_type.__name__
        return data

    def get_final_serializer(self, value):
        serializer = None
        if isinstance(value, UserAgeQuestion):
            serializer = UserAgeQuestionSerializer(value)
        if isinstance(value, BooleanQuestion):
            serializer = BooleanQuestionSerializer(value)
        return serializer

class MultipleChoicesSerializer(serializers.ModelSerializer):
    choices = ChoiceField(many=True)
    class Meta:
        fields = ('basechoicefield_set',)
        depth = 1


class BooleanQuestionSerializer(MultipleChoicesSerializer):
    class Meta(MultipleChoicesSerializer.Meta): 
        model = BooleanQuestion


class UserAgeQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAgeQuestion

class SurveySerializer(serializers.ModelSerializer):
    elements = ThematicElementField(many=True, source='thematicelement_set')
    class Meta:
        model = Thematic
        fields = ('id', 'title', 'elements')
        depth = 1

