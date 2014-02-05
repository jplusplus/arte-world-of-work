# all API endpoints test should go here 
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from app.core.models import *
from datetime import datetime

class AccountTests(APITestCase):
    # ------------------------------------------------------------------------- 
    # Utility methods
    def assetLenIs(self, enum, size):
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


    def test_get_survey(self):
        # import pdb; pdb.set_trace()
        url = reverse('survey-list')
        response = self.client.get(url)
        all_thematics = response.data
        self.assetLenIs(all_thematics, 2)
        for thematic in all_thematics:
            # contract on arguments present
            self.assertIsNotNone(thematic.get('elements', None))
            self.assertIsNotNone(thematic.get('id',       None))
            self.assertIsNotNone(thematic.get('title',    None))

            if thematic['id'] == self.thematic1:
                self.assertLenIs(thematic.elements, 6)
                self.assertModelIn(thematic.elements, self.question1)
                self.assertModelIn(thematic.elements, self.question2)
                self.assertModelIn(thematic.elements, self.question3)
                self.assertModelIn(thematic.elements, self.question4)


            for sub_element in thematic.get('elements'): 
                self.assertAttrNotNone(sub_element, 'position')
                self.assertAttrNotNone(sub_element, 'type')
                self.assertIn(sub_element['type'], ('feedback','question'))
                try:
                    self.assertIsNotNone(sub_element.get('position', None))
                except Exception, e:
                    self.debug("Element doesn't have a position: %s" % sub_element)
                    raise e
