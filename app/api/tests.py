# all API endpoints test should go here 
from django.contrib.auth import get_user_model
User = get_user_model()
from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework.serializers import ModelSerializer
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from app.core.models import *
from app.utils import TestCaseMixin
from app.api import mixins 

def init(instance):
    # auth & client setup
    instance.user = User.objects.create()
    instance.anon_client = APIClient()
    instance.authed_client = APIClient()
    token, created = Token.objects.get_or_create(user=instance.user)
    instance.authed_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    # thematics 
    instance.thematic1 = Thematic.objects.create(position=1, title='You')
    instance.thematic2 = Thematic.objects.create(position=2, title='Your Work')

    # thematic1 question and feedback 
    instance.question1 = instance.createQuestion(TypedNumberQuestion, **{'unit': '%'})
    instance.question2 = instance.createQuestion(BooleanQuestion)
    instance.question3 = instance.createQuestion(TextSelectionQuestion)
    instance.question4 = instance.createQuestion(TypedNumberQuestion, **{'unit': '%'})

    default_source = {'source_url': 'http://jplusplus.org', 'source_title': 'Jpp website' }
    instance.feedback1 = instance.createFeedback(StaticFeedback, **default_source)
    instance.feedback2 = instance.createFeedback(StaticFeedback, **default_source)

    # question 3 choices
    instance.question3_choice1 = instance.createChoice(instance.question3, TextChoiceField)
    instance.question3_choice2 = instance.createChoice(instance.question3, TextChoiceField)
    instance.question3_choice3 = instance.createChoice(instance.question3, TextChoiceField)

    instance.question1.set_thematic(instance.thematic1, 1) 
    instance.question2.set_thematic(instance.thematic1, 2) 
    instance.question3.set_thematic(instance.thematic1, 3) 
    instance.question4.set_thematic(instance.thematic1, 4)

    instance.feedback1.set_thematic(instance.thematic1, 5)
    instance.feedback2.set_thematic(instance.thematic1, 6) 

    # thematic 2 question
    instance.question5 = instance.createQuestion(MediaSelectionQuestion, media_type='icon')
    instance.question5_choice1 = instance.createChoice(instance.question5, MediaChoiceField, picture='pict1')
    instance.question5_choice2 = instance.createChoice(instance.question5, MediaChoiceField, picture='pict2')
    instance.question5_choice3 = instance.createChoice(instance.question5, MediaChoiceField, picture='pict3')
    instance.question5_choice4 = instance.createChoice(instance.question5, MediaChoiceField, picture='pict3')
    instance.question5.set_thematic(instance.thematic2, 1)

    # answers creation
    instance.answer1 = instance.question1.create_answer(user=instance.user, value=2)
    instance.answer2 = instance.question2.create_answer(user=instance.user, value=instance.question2.choices()[0])


class TestUtils(object):
    def createQuestion(self, klass=None, **kwargs):
        kwargs['label']     = kwargs.get('label', 'Default label')
        kwargs['hint_text'] = kwargs.get('hint_text', 'Default hint text')
        return self.createModelInstance(klass, **kwargs)

    def createFeedback(self, klass=None, **kwargs):
        kwargs['html_sentence'] = kwargs.get('html_sentence', 
            'Default <strong>html_sentence</strong>')
        return self.createModelInstance(klass, **kwargs)

    def createChoice(self, question, klass, **kwargs):
        kwargs['title'] = kwargs.get('title', 'Default title')
        kwargs['question'] = question
        return self.createModelInstance(klass, **kwargs)

    def findElement(self, enum=[], elem_id=None):
        result = None
        for elem in enum:
            if elem.get('id', None) == elem_id: 
                result = elem 
        return result

class ThematicTests(APITestCase, TestCaseMixin, TestUtils):

    def setUp(self):
        init(self)

    def test_list_thematic(self):
        url = reverse('thematic-list')
        response = self.client.get(url)
        all_thematics = response.data
        for thematic in all_thematics:
            # contract on arguments present
            self.assertAttrNotNone(thematic, 'elements')
            self.assertAttrNotNone(thematic, 'id')
            self.assertAttrNotNone(thematic, 'title')

    def test_list_thematic_nested(self):
        url = reverse('thematic-nested-list')
        response = self.client.get(url)
        all_thematics = response.data
        for thematic in all_thematics:
            # contract on arguments present
            self.assertAttrNotNone(thematic, 'elements')
            self.assertAttrNotNone(thematic, 'id')
            self.assertAttrNotNone(thematic, 'title')
            for element in thematic.get('elements'):
                self.assertAttrNotNone(element, 'position')
                self.assertAttrNotNone(element, 'type')
                self.assertIn(element['type'], ('feedback','question'))

    def test_thematic_nested_detail(self):
        url = reverse('thematic-nested-detail', kwargs={ 'pk': self.thematic1.pk})
        response = self.client.get(url)
        thematic = response.data
        sub_elements = thematic.get('elements')
        self.assertLenIs(sub_elements, 6)
        question1_elem = sub_elements[0]
        question2_elem = sub_elements[1]
        question3_elem = sub_elements[2]
        question4_elem = sub_elements[3]
        feedback1_elem = sub_elements[4]
        feedback2_elem = sub_elements[5]

        self.assertEqual(question1_elem.get('type'), 'question')
        self.assertEqual(question1_elem.get('typology'), 'typed_number')
        self.assertEqual(question1_elem.get('object_id'), self.question1.id)

        self.assertEqual(question2_elem.get('type'), 'question')
        self.assertEqual(question2_elem.get('typology'), 'boolean')
        self.assertEqual(question2_elem.get('object_id'), self.question2.id)

        self.assertEqual(question3_elem.get('type'), 'question')
        self.assertEqual(question3_elem.get('typology'), 'text_selection')
        self.assertEqual(question3_elem.get('object_id'), self.question3.id)
        self.assertAttrNotNone(question3_elem, 'validate_button_label')


        self.assertEqual(question4_elem.get('type'), 'question')
        self.assertEqual(question4_elem.get('typology'), 'typed_number')
        self.assertEqual(question4_elem.get('object_id'), self.question4.id)
        
        self.assertEqual(feedback1_elem.get('type'), 'feedback')
        self.assertEqual(feedback1_elem.get('sub_type'), 'static')
        self.assertEqual(feedback1_elem.get('object_id'), self.feedback1.id)
        
        self.assertEqual(feedback2_elem.get('type'), 'feedback')
        self.assertEqual(feedback2_elem.get('sub_type'), 'static')
        self.assertEqual(feedback2_elem.get('object_id'), self.feedback2.id)

    def test_thematic_nested_detail_with_pictures(self):
        url = reverse('thematic-nested-detail', kwargs={ 'pk': self.thematic2.pk})
        response = self.client.get(url)
        thematic = response.data
        sub_elements = thematic.get('elements')
        question = sub_elements[0]
        self.assertAttrNotNone(question, 'validate_button_label')
        self.assertEqual(question['type'], 'question')
        for choice in question.get('choices'):
            self.assertAttrNotNone(choice, 'title')
            self.assertAttrNotNone(choice, 'picture')


class AnswerTestCase(APITestCase, TestCaseMixin, TestUtils):
    def setUp(self):
        init(self)

    def test_list_my_answers_auth(self):
        list_url = reverse('my-answers-list')
        response = self.authed_client.get(list_url)
        self.assertEqual(response.status_code, 200)
        answers = response.data
        self.assertLenIs(answers,  2)

    def test_list_my_answers_anon(self):
        list_url = reverse('my-answers-list')
        response = self.anon_client.get(list_url)
        self.assertEqual(response.status_code, 401)
    
    def test_create_anonymous(self):
        url = reverse('answer-list')
        data = {
            'value': 20,
            'question': self.question1.pk
        }
        response = self.anon_client.post(url, data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_create_typed_number_success(self):
        url = reverse('answer-list')
        data = {
            'value': 20,
            'question': self.question1.pk,
        }
        response = self.authed_client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        answer = response.data
        self.assertEqual(answer['user'], self.user.pk)


    def test_create_typed_number_out_of_range(self):
        url = reverse('answer-list')
        data = {
            'value': 400, # max number is 100 by default, it should work
            'question': self.question1.pk,
        }
        response = self.authed_client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_create_selection_answer_success(self):
        url = reverse('answer-list')
        data = {
            'value': [ self.question3_choice1.pk, self.question3_choice2.pk ],
            'question': self.question3.pk
        }
        response = self.authed_client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)   

    def test_create_selection_answer_no_choice(self):
        url = reverse('answer-list')
        data = {
            'value': [],
            'question': self.question3.pk
        }
        response = self.authed_client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_create_selection_answer_unrelated_choice(self):
        url = reverse('answer-list')
        data = {
            'value': [self.question5_choice1.pk],
            'question': self.question3.pk
        }
        response = self.authed_client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_thematic_results_list(self):
        url = reverse('thematic-results-list')
        response = self.authed_client.get(url)
        self.assertEqual(response.status_code, 200)
        thematics = response.data
        self.assertLenIs(thematics, 2)


    def test_thematic_results_detail(self):
        url = reverse('thematic-results-detail', kwargs={'pk': self.thematic1.pk })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        thematic = response.data
        self.assertIsNotNone(thematic)


class UserTestCase(APITestCase, TestCaseMixin):
    def setUp(self):
        self.user = User.objects.create()
        self.client = APIClient()
        token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_post_user_list(self):
        url = reverse('user-list')
        result = self.client.post(url)
        self.assertEqual(result.status_code, 201)

        data = result.data
        self.assertAttrNotNone(data, 'profile')

    # def test_user_auth():
        # url = reverse('user-auth')

    def test_user_mypostion(self):
        url = reverse('user-mypostion', kwargs={'pk': self.user.pk})
        result = self.client.get(url)
        self.assertIsNotNone(result)


class TypedNumberSerializer(ModelSerializer):
    class Meta:
        model = TypedNumberQuestion

class TestSerializer(mixins.ContentTypeMixin, ModelSerializer):
    ctype_mapping = {
        TypedNumberQuestion: TypedNumberSerializer,
    }
    class Meta:
        model = BaseQuestion

class MixinsTestCase(TestCase, TestCaseMixin, TestUtils):

    def setUp(self):
        self.thematic = Thematic.objects.create(position=1, title='You')
        self.question = self.createQuestion(TypedNumberQuestion, **{'unit': '%'})
        self.question.set_thematic(self.thematic, 1) 

    def test_get_generic(self):
        question = BaseQuestion.objects.get(pk=self.question.pk)
        serializer = TestSerializer(question)
        ctype, cobject = serializer.get_generic(question)
        self.assertEqual(ctype, self.question.content_type)
        self.assertEqual(cobject, self.question)

    def test_get_ctype_serializer(self):
        question = BaseQuestion.objects.get(pk=self.question.pk)
        serializer = TestSerializer(question)
        final_serializer = serializer.get_ctype_serializer(question)
        self.assertEqual(final_serializer, TypedNumberSerializer)

    def test_serialize(self):
        data = TestSerializer(self.question).data
        # should contain all basic question informations
        self.assertAttrNotNone(data, 'label')
        self.assertAttrNotNone(data, 'skip_button_label')
        self.assertAttrNotNone(data, 'hint_text')

        # and all typed number information
        self.assertAttrNotNone(data, 'min_number')
        self.assertAttrNotNone(data, 'max_number')
        self.assertAttrNotNone(data, 'unit')
