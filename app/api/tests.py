# all API endpoints test should go here 
from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.urlresolvers import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from app.core.models import *
from app.utils import TestCaseMixin

def init(instance):
    default_source = {'source_url': 'http://jplusplus.org', 'source_title': 'Jpp website' }

    instance.thematic1 = Thematic.objects.create(position=0, title='You')
    instance.thematic2 = Thematic.objects.create(position=1, title='Your Work')

    # thematic1 question and feedback 
    instance.question1 = instance.createQuestion(TypedNumberQuestion, **{'unit': '%'})
    instance.question2 = instance.createQuestion(BooleanQuestion)
    instance.question3 = instance.createQuestion(TextSelectionQuestion)
    instance.question4 = instance.createQuestion(TypedNumberQuestion, **{'unit': '%'})

    instance.feedback1 = instance.createFeedback(StaticFeedback, **default_source)
    instance.feedback2 = instance.createFeedback(StaticFeedback, **default_source)

    # question 3 choices
    instance.question3_choice1 = instance.createChoice(instance.question3, TextChoiceField)
    instance.question3_choice2 = instance.createChoice(instance.question3, TextChoiceField)
    instance.question3_choice2 = instance.createChoice(instance.question3, TextChoiceField)

    instance.question1.set_thematic(instance.thematic1, 0) 
    instance.question2.set_thematic(instance.thematic1, 1) 
    instance.question3.set_thematic(instance.thematic1, 2) 
    instance.question4.set_thematic(instance.thematic1, 3)

    instance.feedback1.set_thematic(instance.thematic1, 4)
    instance.feedback2.set_thematic(instance.thematic1, 5) 

    # thematic 2 question
    instance.question5 = instance.createQuestion(MediaSelectionQuestion, media_type='icon')
    instance.question5_choice1 = instance.createChoice(instance.question5, MediaChoiceField, picture='pict1')
    instance.question5_choice2 = instance.createChoice(instance.question5, MediaChoiceField, picture='pict2')
    instance.question5_choice3 = instance.createChoice(instance.question5, MediaChoiceField, picture='pict3')
    instance.question5_choice4 = instance.createChoice(instance.question5, MediaChoiceField, picture='pict3')
    instance.question5.set_thematic(instance.thematic2)


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
        self.user = User.objects.create()
        self.anon_client = APIClient()
        self.authed_client = APIClient()
        token, created = Token.objects.get_or_create(user=self.user)
        self.authed_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.answer1 = self.question1.create_answer(user=self.user, value=2)
        self.answer2 = self.question2.create_answer(user=self.user, value=self.question2.choices()[0])

    def test_list_my_answers_auth(self):
        # expect HTTP_OK - 200
        list_url = reverse('answer-list')
        response = self.authed_client.get(list_url)
        self.assertEqual(response.status_code, 200)
        answers = response.data
        self.assertLenIs(answers,  2)


    def test_create_authenticated(self):
        # expected: HTTP 201
        pass

    def test_create_anonymous(self):
        # expected: HTTP 403
        pass


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
        # pass

