# all API endpoints test should go here 
from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.urlresolvers import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from app.core.models import *
from app.utils import TestCaseMixin


class ThematicTests(APITestCase, TestCaseMixin):
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

    def setUp(self):
        default_source = {'source_url': 'http://jplusplus.org', 'source_title': 'Jpp website' }
        # thematics 
        self.thematic1 = Thematic.objects.create(position=0, title='You')
        self.thematic2 = Thematic.objects.create(position=1, title='Your Work')

        # thematic1 question and feedback 
        self.question1 = self.createQuestion(TypedNumberQuestion, **{'unit': '%'})
        self.question2 = self.createQuestion(BooleanQuestion)
        self.question3 = self.createQuestion(TextSelectionQuestion)
        self.question4 = self.createQuestion(TypedNumberQuestion, **{'unit': '%'})

        self.feedback1 = self.createFeedback(StaticFeedback, **default_source)
        self.feedback2 = self.createFeedback(StaticFeedback, **default_source)
        
        # question 3 choices
        self.question3_choice1 = self.createChoice(self.question3, TextChoiceField)
        self.question3_choice2 = self.createChoice(self.question3, TextChoiceField)
        self.question3_choice2 = self.createChoice(self.question3, TextChoiceField)

        self.question1.set_thematic(self.thematic1, 0) 
        self.question2.set_thematic(self.thematic1, 1) 
        self.question3.set_thematic(self.thematic1, 2) 
        self.question4.set_thematic(self.thematic1, 3)

        self.feedback1.set_thematic(self.thematic1, 4)
        self.feedback2.set_thematic(self.thematic1, 5) 


    def test_list_thematic(self):
        # import pdb; pdb.set_trace()
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

        self.assertEqual(question4_elem.get('type'), 'question')
        self.assertEqual(question4_elem.get('typology'), 'typed_number')
        self.assertEqual(question4_elem.get('object_id'), self.question4.id)
        
        self.assertEqual(feedback1_elem.get('type'), 'feedback')
        self.assertEqual(feedback1_elem.get('sub_type'), 'static')
        self.assertEqual(feedback1_elem.get('object_id'), self.feedback1.id)
        
        self.assertEqual(feedback2_elem.get('type'), 'feedback')
        self.assertEqual(feedback2_elem.get('sub_type'), 'static')
        self.assertEqual(feedback2_elem.get('object_id'), self.feedback2.id)


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

