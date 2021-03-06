# all API endpoints test should go here 
from django.contrib.auth import get_user_model
User = get_user_model()
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.db.models.signals    import post_save
from rest_framework.serializers import ModelSerializer
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from app.core         import transport
from app.core.models  import *
from app.core.signals import create_boolean_choices
from app.core.signals import create_user_choice_fields

from app.utils import receiver_subclasses
from app.utils import TestCaseMixin
from app.api import mixins 

from app.core.signals            import create_generic_element
from app.core.signals            import create_thematic_element

@receiver_subclasses(post_save, BaseQuestion, "basequestion_post_save")
@receiver_subclasses(post_save, BaseFeedback, "basefeedback_post_save")
def _create_generic_element(sender, **kwargs):
    create_generic_element(sender, **kwargs)

@receiver_subclasses(post_save, ThematicElement, "thematicelement_post_save")
def _create_thematic_element(sender, **kwargs):
    create_thematic_element(sender, **kwargs)

def init(instance):
    post_save.connect(create_boolean_choices,    sender=BooleanQuestion)
    post_save.connect(create_user_choice_fields, sender=UserGenderQuestion)

    # auth & client setup
    instance.user = User.objects.create()
    instance.anon_client = APIClient()
    instance.authed_client = APIClient()
    token, created = Token.objects.get_or_create(user=instance.user)
    instance.authed_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    # thematics 
    instance.thematic1     = Thematic.objects.create(position=1, title='You')
    instance.thematic2     = Thematic.objects.create(position=2, title='Your Work')

    # thematic1 question and feedback 
    instance.question1 = instance.createQuestion(TypedNumberQuestion, **{'unit': '%'})
    instance.question2 = instance.createQuestion(BooleanQuestion)
    instance.question3 = instance.createQuestion(TextSelectionQuestion)
    instance.question4 = instance.createQuestion(TypedNumberQuestion, **{'unit': '%'})

    default_source = {'source_url': 'http://jplusplus.org', 'source_title': 'Jpp website' }
    instance.feedback1 = instance.createFeedback(instance.question1, StaticFeedback, **default_source)
    instance.feedback2 = instance.createFeedback(instance.question2, StaticFeedback, **default_source)

    # question 3 choices
    instance.question3_choice1 = instance.createChoice(instance.question3, TextChoiceField, position=1)
    instance.question3_choice2 = instance.createChoice(instance.question3, TextChoiceField, position=2)
    instance.question3_choice3 = instance.createChoice(instance.question3, TextChoiceField, position=3)

    instance.question1.set_thematic(instance.thematic1, 1) 
    instance.question2.set_thematic(instance.thematic1, 2) 
    instance.question3.set_thematic(instance.thematic1, 3) 
    instance.question4.set_thematic(instance.thematic1, 4)

    # thematic 2 question
    instance.question5 = instance.createQuestion(MediaSelectionQuestion, media_type='icon')
    instance.question5_choice1 = instance.createChoice(instance.question5, MediaChoiceField, picture='pict1', position=1)
    instance.question5_choice2 = instance.createChoice(instance.question5, MediaChoiceField, picture='pict2', position=2)
    instance.question5_choice3 = instance.createChoice(instance.question5, MediaChoiceField, picture='pict3', position=3)
    instance.question5_choice4 = instance.createChoice(instance.question5, MediaChoiceField, picture='pict3', position=4)
    instance.question5.set_thematic(instance.thematic2, 1)

    # answers creation
    if getattr(instance, 'do_create_answers', None) != False:
        instance.answer1 = instance.question1.create_answer(user=instance.user, value=2)
        instance.answer2 = instance.question2.create_answer(user=instance.user, value=instance.question2.choices()[0])


     # user thematic & user questions
    instance.user_thematic = Thematic.objects.create(position=3, title='You BIS')

    instance.user_age_question            = instance.createQuestion(UserAgeQuestion)
    instance.user_gender_question         = instance.createQuestion(UserGenderQuestion)
    instance.user_native_country_question = instance.createQuestion(UserCountryQuestion, **{ 'profile_attribute': 'native_country' })
    instance.user_living_country_question = instance.createQuestion(UserCountryQuestion, **{ 'profile_attribute': 'living_country' })

    instance.user_age_question.set_thematic(instance.user_thematic, 1)
    instance.user_gender_question.set_thematic(instance.user_thematic, 2)
    instance.user_native_country_question.set_thematic(instance.user_thematic, 3)
    instance.user_living_country_question.set_thematic(instance.user_thematic, 4)


class TestUtils(object):
    def createQuestion(self, klass=None, **kwargs):
        kwargs['label']     = kwargs.get('label', 'Default label')
        kwargs['hint_text'] = kwargs.get('hint_text', 'Default hint text')
        return self.createModelInstance(klass, **kwargs)

    def createFeedback(self, question, klass=None, **kwargs):
        kwargs['html_sentence'] = kwargs.get('html_sentence', 
            'Default <strong>html_sentence</strong>')
        kwargs['question'] = question
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
        self.assertLenIs(sub_elements, 4)
        question1_elem = sub_elements[0]
        question2_elem = sub_elements[1]
        question3_elem = sub_elements[2]
        question4_elem = sub_elements[3]
        
        # Question 1 
        self.assertAttrEqual(question1_elem, 'type',      'question')
        self.assertAttrEqual(question1_elem, 'typology',  'typed_number')
        self.assertAttrEqual(question1_elem, 'object_id', self.question1.id)

        # Question 1 feedback
        feedback1 = question1_elem['feedback']
        self.assertAttrEqual(feedback1, 'type',     'feedback' )
        self.assertAttrEqual(feedback1, 'sub_type', 'static')

        self.assertAttrEqual(question2_elem, 'type',      'question')
        self.assertAttrEqual(question2_elem, 'typology',  'boolean')
        self.assertAttrEqual(question2_elem, 'object_id', self.question2.id)

        self.assertAttrEqual(question3_elem, 'type',      'question')
        self.assertAttrEqual(question3_elem, 'typology',  'text_selection')
        self.assertAttrEqual(question3_elem, 'object_id', self.question3.id)


        self.assertAttrEqual(question4_elem, 'type',      'question')
        self.assertAttrEqual(question4_elem, 'typology',  'typed_number')
        self.assertAttrEqual(question4_elem, 'object_id', self.question4.id)

    def test_thematic_nested_detail_with_pictures(self):
        url = reverse('thematic-nested-detail', kwargs={ 'pk': self.thematic2.pk})
        response = self.client.get(url)
        thematic = response.data
        sub_elements = thematic.get('elements')
        question = sub_elements[0]
        self.assertEqual(question['type'], 'question')
        for choice in question.get('choices'):
            self.assertAttrNotNone(choice, 'title')
            self.assertAttrNotNone(choice, 'picture')

    def test_thematic_nested_user_questions(self):
        url = reverse('thematic-nested-detail', kwargs={ 'pk': self.user_thematic.pk})
        response = self.client.get(url)
        thematic = response.data
        sub_elements = thematic.get('elements')

        user_age_question = sub_elements[0]
        user_gender_question = sub_elements[1]
        user_native_country_question = sub_elements[2]
        user_living_country_question = sub_elements[3]

        genders = user_gender_question['choices']
        male    = filter( lambda g: g['value'] == 'male', genders  )[0]
        female  = filter( lambda g: g['value'] == 'female', genders)[0]
        self.assertIsNotNone( male   )    
        self.assertIsNotNone( female )


class AnswerTestCase(APITestCase, TestCaseMixin, TestUtils):
    # utility method for user answers, keeping it DRY
    def run_update_user_answer(self, question_klass, attr_name, values, **kwargs):
        question_kwargs = kwargs.get('question_init', {})
        user = User.objects.create()
        client = self.setupClient(user)
        question = self.createQuestion(question_klass, **question_kwargs)
        answer = question.create_answer(user=user,value=values[0])
        profile = UserProfile.objects.get(user=user)
        self.assertAttrEqual(profile, attr_name, values[0]) # security check
        url = reverse('answer-detail', kwargs={'pk': answer.pk})
        data = {
            'question': question.id,
            'value': values[1]
        }
        response = client.put(url, data, format='json')
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(response.status_code, 200)
        self.assertAttrEqual(profile, attr_name, values[1]) # security check

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
        self.assertIn(response.status_code, (200, 201))
        answer = response.data
        self.assertAttrEqual(answer, 'user',     self.user.pk)
        self.assertAttrEqual(answer, 'question', self.question1.pk)
        self.assertAttrEqual(answer, 'value',    20)

    def test_create_typed_number_multiple_success(self):
        # special case for user trying to create an answer for an already
        # answered question. We want to be sure that the answer have been
        # updated and not created 
        url = reverse('answer-list')
        data1 = {
            'value': 20,
            'question': self.question1.pk,
        }
        data2 = {
            'value': 60,
            'question': self.question1.pk,
        }
        response1 = self.authed_client.post(url, data1, format='json')
        response2 = self.authed_client.post(url, data2, format='json')

        self.assertIn(response1.status_code, (200, 201))
        self.assertIn(response2.status_code, (200, 201))

        answer1 = response1.data
        self.assertAttrEqual(answer1, 'user',     self.user.pk)
        self.assertAttrEqual(answer1, 'question', self.question1.pk)
        self.assertAttrEqual(answer1, 'value',    20)

        answer2 = response2.data
        self.assertAttrEqual(answer2, 'user',     self.user.pk)
        self.assertAttrEqual(answer2, 'question', self.question1.pk)
        self.assertAttrEqual(answer2, 'value',    60)

        user_answers = BaseAnswer.objects.filter(user=self.user.pk, question=self.question1.pk)
        self.assertEqual(user_answers.count(), 1)


    


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

    def test_create_user_age_answer(self):
        url = reverse('answer-list')
        data = {
            'value': 24,
            'question': self.user_age_question.pk
        }
        response = self.authed_client.post(url, data, format='json')
        profile  = UserProfile.objects.get(user=self.user) 
        self.assertEqual(response.status_code, 201)
        self.assertEqual(profile.age, 24)

    def test_update_user_age_answer(self):
        self.run_update_user_answer(question_klass=UserAgeQuestion, 
                                    values=(20, 24),
                                    attr_name='age')

    def test_create_user_gender_answer(self):
        url = reverse('answer-list')
        data = {
            'value': 'female',
            'question': self.user_gender_question.pk
        }
        response = self.authed_client.post(url, data, format='json')
        profile  = UserProfile.objects.get(user=self.user) 
        self.assertEqual(response.status_code, 201)
        self.assertEqual(profile.gender, 'female')

    def test_update_user_gender_answer(self):
        self.run_update_user_answer(question_klass=UserGenderQuestion, 
                                    values=('male', 'female'),
                                    attr_name='gender')

    def test_create_user_living_country(self):
        url = reverse('answer-list')
        data = {
            'value': 'BE',
            'question': self.user_living_country_question.pk
        }
        response = self.authed_client.post(url, data, format='json')
        profile  = UserProfile.objects.get(user=self.user) 
        self.assertEqual(response.status_code, 201)
        self.assertEqual(profile.living_country, 'BE')

    def test_update_user_living_country(self):
        self.run_update_user_answer(question_klass=UserCountryQuestion, 
                                    question_init={
                                        'profile_attribute': 'living_country'},
                                    values=('FR', 'BE'),
                                    attr_name='living_country')


    def test_create_user_native_country(self):
        url = reverse('answer-list')
        data = {
            'value': 'DE',
            'question': self.user_native_country_question.pk
        }
        response = self.authed_client.post(url, data, format='json')
        profile  = UserProfile.objects.get(user=self.user) 
        self.assertEqual(response.status_code, 201)
        self.assertEqual(profile.native_country, 'DE')

    def test_update_user_native_country(self):
        self.run_update_user_answer(question_klass=UserCountryQuestion,
                                    question_init={
                                        'profile_attribute': 'native_country'},
                                    values=('DE', 'RU'),
                                    attr_name='native_country')

    def test_thematic_results_list(self):
        url = reverse('thematic-results-list')
        response = self.authed_client.get(url)
        self.assertEqual(response.status_code, 200)
        thematics = response.data
        self.assertLenIs(thematics, 3)


    def test_thematic_results_detail(self):
        url = reverse('thematic-results-detail', kwargs={'pk': self.thematic1.pk })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        thematic = response.data
        self.assertIsNotNone(thematic)

class ResultsTestCase(APITestCase, TestCaseMixin, TestUtils):
    def setUp(self):
        self.do_create_answers = False
        self.answers = {}
        init(self) 
        # clean existing answers (just in case)
        [ans.delete() for ans in BaseAnswer.objects.all()]
        # special answers for this API test case 
        self.create_answers()

    def create_answers(self):
        q1 = self.question1
        self.add_answer(q1, 15)
        self.add_answer(q1, 18)
        self.add_answer(q1, 19)
        self.add_answer(q1, 20)
        self.add_answer(q1, 21)
        self.add_answer(q1, 45)
        self.add_answer(q1, 45)
        self.add_answer(q1, 45)
        self.add_answer(q1, 70)
        self.add_answer(q1, 75)

        q2 = self.question2 
        yes_q2 = q2.choices().filter(title='yes')[0]
        no_q2 = q2.choices().filter(title='no')[0]

        self.add_answer(q2, yes_q2)
        self.add_answer(q2, yes_q2)
        self.add_answer(q2, yes_q2)
        self.add_answer(q2, yes_q2)
        self.add_answer(q2, yes_q2)
        self.add_answer(q2, yes_q2)
        self.add_answer(q2, yes_q2)
        
        self.add_answer(q2, no_q2)
        self.add_answer(q2, no_q2)
        self.add_answer(q2, no_q2)

        q3 = self.question3 
        q3_c1, q3_c2, q3_c3 = q3.choices()
        self.add_answer(q3, q3_c1)
        self.add_answer(q3, q3_c1)
        self.add_answer(q3, q3_c1)

        self.add_answer(q3, q3_c2)
        self.add_answer(q3, q3_c2)
        
        self.add_answer(q3, q3_c3)
        self.add_answer(q3, q3_c3)
        self.add_answer(q3, q3_c3)
        self.add_answer(q3, q3_c3)
        self.add_answer(q3, q3_c3)

    def add_answer(self, question, value, user=None):
        if user == None:
            user = User.objects.create()
        self.answers[question.id] = question.create_answer(user=user, value=value)

    def test_results_not_found(self):
        url = reverse('question-results', kwargs={ 'pk': 99 })
        response = self.client.get(url) 
        self.assertEqual(response.status_code, 404)
        
        
    def test_typed_number_question_results(self):
        url = reverse('question-results', kwargs={ 'pk': self.question1.pk })
        response = self.client.get(url) 
        self.assertEqual(response.status_code, 200)
        question = response.data
        results  = question.get('results')

        self.assertEqual(results.get('chart_type'), transport.CHART_TYPES.HISTOGRAMME)
        self.assertEqual(results.get('total_answers'), 10)
        sets = results.get('sets')
        self.assertEqual( sets[1]['min'], 0 )
        self.assertEqual( sets[1]['max'], 20 )

        self.assertEqual( sets[2]['min'], 20 )
        self.assertEqual( sets[2]['max'], 40 )

        self.assertEqual( sets[3]['min'], 40 )
        self.assertEqual( sets[3]['max'], 60 )

        self.assertEqual( sets[4]['min'], 60 )
        self.assertEqual( sets[4]['max'], 80 )


        self.assertEqual( sets[5]['min'], 80  )
        self.assertEqual( sets[5]['max'], 100 )

        results = results['results'] 

        self.assertEqual( results[1], 30 )
        self.assertEqual( results[2], 20 )
        self.assertEqual( results[3], 30 )
        self.assertEqual( results[4], 20 )
        self.assertEqual( results[5], 0  )

    def test_boolean_question_results(self):
        question   = self.question2
        yes_choice = question.choices().get(title='yes')
        no_choice  = question.choices().get(title='no' )

        url = reverse('question-results', kwargs={ 'pk': question.pk })
        response        = self.client.get(url) 
        self.assertEqual(response.status_code, 200)
        question        = response.data
        results_object  = question.get('results')

        results = results_object.get('results')
        sets    = results_object.get('sets')

        self.assertAttrEqual(results_object, 'chart_type', transport.CHART_TYPES.PIE)
        self.assertAttrEqual(results_object, 'total_answers', 10)
        self.assertIsNotNone( sets[ yes_choice.pk ] )
        self.assertEqual( sets[ yes_choice.pk ]['title'], yes_choice.title )
        self.assertEqual( results[ yes_choice.pk ], 70)

        self.assertIsNotNone( sets[ no_choice.pk ] )
        self.assertEqual( sets[ no_choice.pk ]['title'], no_choice.title )
        self.assertEqual( results[ no_choice.pk ], 30)

    def test_selection_question_results(self):
        question   = self.question3 
        choice1    = self.question3_choice1
        choice2    = self.question3_choice2
        choice3    = self.question3_choice3
        
        url = reverse('question-results', kwargs={ 'pk': question.pk })
        response        = self.client.get(url) 
        self.assertEqual(response.status_code, 200)
        question_json = response.data
        results_object = question_json.get('results')
        results        = results_object.get('results')
        sets           = results_object.get('sets')

        self.assertAttrEqual(results_object, 'chart_type', transport.CHART_TYPES.HORIZONTAL_BAR)
        self.assertAttrEqual(results_object, 'total_answers', 10)

        self.assertIsNotNone( sets[choice1.pk] )
        self.assertEqual(     sets[choice1.pk]['title'], choice1.title )
        self.assertEqual(     results[choice1.pk], 30)

        self.assertIsNotNone( sets[ choice2.pk ] )
        self.assertEqual( sets[ choice2.pk ]['title'], choice2.title )
        self.assertEqual( results[ choice2.pk ], 20)

        self.assertIsNotNone( sets[ choice3.pk ] )
        self.assertEqual( sets[ choice3.pk ]['title'], choice3.title )
        self.assertEqual( results[ choice3.pk ], 50)

    def test_dynamic_feedback(self):
        client = APIClient()
        user = User.objects.create()
        token, created = Token.objects.get_or_create(user=user)
        client.force_authenticate(user=user, token=token)
        question = self.question1
        url      = reverse('question-feedback', kwargs={ 'pk': question.pk })
        response = client.get(url)

        feedback = response.data
        self.assertAttrEqual(  feedback, 'type',     'feedback')
        self.assertAttrEqual(  feedback, 'sub_type', 'dynamic')
        self.assertAttrNotNone(feedback, 'html_sentence')
        self.assertAttrNotNone(feedback, 'question')
        self.assertAttrEqual(feedback['question'], 'id', question.pk)


class CountriesTestCase(APITestCase, TestCaseMixin):
    def test_list_countries(self):
        url = reverse('country-list')
        response = self.client.get(url)
        countries = response.data
        self.assertTrue(len(countries) > 0)
        for country in countries:
            self.assertEqual(type(country['name']), type(u''))


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
        self.assertAttrNotNone(data, 'token')

    def test_user_mypostion(self):
        url = reverse('my-position')
        response = self.client.get(url)
        position = response.data
        self.assertEqual(response.status_code, 200)
        self.assertAttrNotNone(position, 'thematic_position')
        self.assertAttrNotNone(position, 'element_position')

class AuthTestCase(APITestCase, TestCaseMixin):
    def setUp(self):
        self.user = User.objects.create()
        self.client = APIClient()
        token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.notAuthClient = APIClient()

        self.fakeAuthClient = APIClient()
        self.fakeAuthClient.credentials(HTTP_AUTHORIZATION='Token justAFakeToken123')

    def test_auth(self):
        url = reverse('verify-token')
        result = self.client.post(url)

        self.assertEqual(result.status_code, 200)

    def test_no_auth(self):
        url = reverse('verify-token')
        result = self.notAuthClient.post(url)

        self.assertEqual(result.status_code, 401)

    def test_fake_auth(self):
        url = reverse('verify-token')
        result = self.fakeAuthClient.post(url)

        self.assertEqual(result.status_code, 401)

# these are test serializer
class TypedNumberSerializer(ModelSerializer):
    class Meta:
        model = TypedNumberQuestion

class TestSerializer(mixins.GenericModelMixin, ModelSerializer):
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
        self.assertAttrNotNone(data, 'hint_text')

        # and all typed number information
        self.assertAttrNotNone(data, 'min_number')
        self.assertAttrNotNone(data, 'max_number')
        self.assertAttrNotNone(data, 'unit')





