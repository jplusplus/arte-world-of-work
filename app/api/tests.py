# all API endpoints test should go here 
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from app.core.models import *
from datetime import datetime

class SurveyTests(APITestCase):
    # ------------------------------------------------------------------------- 
    # Utility methods
    # ------------------------------------------------------------------------- 
    def assertLenIs(self, enum, size):
        # check the passed `enum` has the appropriated length 
        self.assertEqual(len(enum), size)

    def assertModelIn(self, enum, model_instance):
        # check the element with `pk` is in `enum`
        self.assertIsNotNone(self.findElement(enum, model_instance.pk))

    def assertAttrNotNone(self, elem, attr):
        self.assertIsNotNone(elem.get(attr, None))

    def debug(self, msg):
        print "\n[DBG - {time}] {msg}".format(time=datetime.now(), msg=msg)

    def createModelInstance(self, klass, **kwargs):
        elem = klass.objects.create(**kwargs)
        elem.save()
        return elem

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
        self.thematic2 = Thematic.objects.create(position=0, title='Your Work')
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

        self.question1.set_thematic(self.thematic1) 
        self.question2.set_thematic(self.thematic1) 
        self.question3.set_thematic(self.thematic1) 
        self.question4.set_thematic(self.thematic1) 
        self.feedback1.set_thematic(self.thematic1) 
        self.feedback2.set_thematic(self.thematic1) 


    def test_list_survey(self):
        # import pdb; pdb.set_trace()
        url = reverse('survey-list')
        response = self.client.get(url)
        all_thematics = response.data
        self.assertLenIs(all_thematics, 2)
        for thematic in all_thematics:
            # contract on arguments present
            self.assertAttrNotNone(thematic, 'elements')
            self.assertAttrNotNone(thematic, 'id')
            self.assertAttrNotNone(thematic, 'title')
            sub_elements = thematic.get('elements')
            for sub_element in sub_elements: 
                self.assertAttrNotNone(sub_element, 'position')
                self.assertAttrNotNone(sub_element, 'type')
                self.assertIn(sub_element['type'], ('feedback','question'))

    def test_survey_detail(self):
        url = reverse('survey-detail', kwargs={ 'pk': self.thematic1.pk})
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
        self.assertEqual(question1_elem.get('id'), self.question1.as_element().pk)
        self.assertEqual(question2_elem.get('type'), 'question')
        self.assertEqual(question2_elem.get('id'), self.question2.as_element().pk)
        self.assertEqual(question3_elem.get('type'), 'question')
        self.assertEqual(question3_elem.get('id'), self.question3.as_element().pk)
        self.assertEqual(question4_elem.get('type'), 'question')
        self.assertEqual(question4_elem.get('id'), self.question4.as_element().pk)
        self.assertEqual(feedback1_elem.get('type'), 'feedback')
        self.assertEqual(feedback1_elem.get('id'), self.feedback1.as_element().pk)
        self.assertEqual(feedback2_elem.get('type'), 'feedback')
        self.assertEqual(feedback2_elem.get('id'), self.feedback2.as_element().pk)