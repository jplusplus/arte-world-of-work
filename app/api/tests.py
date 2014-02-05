# all API endpoints test should go here 
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from app.core.models import *

class AccountTests(APITestCase):
    # ------------------------------------------------------------------------- 
    # Utility methods
    def assetLenIs(self, enum, size):
        self.assertEqual(len(enum), size)

    def createQuestion(self, klass=None, **kwargs):
        kwargs['label']     = kwargs.get('label', 'Default label')
        kwargs['hint_text'] = kwargs.get('hint_text', 'Default hint text')
        return klass.objects.create(**kwargs)

    def createFeedback(self, klass=None, **kwargs):
        kwargs['label']     = kwargs.get('label', 'Default label')
        kwargs['hint_text'] = kwargs.get('hint_text', 'Default hint text')
        return klass.objects.create(**kwargs)


    def setUp(self):
        # thematics 
        self.thematic1 = Thematic.objects.create(position=0, title='You')
        self.thematic2 = Thematic.objects.create(position=0, title='Your Work')
        # thematic1 question and feedback 
        self.question1 = self.createQuestion(TypedNumberQuestion, **{'unit': '%'})
        self.question2 = self.createQuestion(BooleanQuestion)
        self.question3 = self.createQuestion(TypedNumberQuestion, **{'unit': '%'})
        self.question4 = self.createQuestion(TypedNumberQuestion, **{'unit': '%'})

        self.thematic1.add_element(self.question1)





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


