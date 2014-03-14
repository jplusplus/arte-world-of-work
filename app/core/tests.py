#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Project : Arte World of Work
# -----------------------------------------------------------------------------
# Author : Pierre Bellon
# -----------------------------------------------------------------------------
# License : proprietary journalism++
# -----------------------------------------------------------------------------
# Creation : 2014-01-10 15:58:02
# Last mod :  2014-01-24 16:59:37
# -----------------------------------------------------------------------------

# all core related tests should go here
from app                         import utils
from app.core                    import transport   
from app.core.models             import * 
from app.core.signals            import create_boolean_choices
from app.core.signals            import create_user_choice_fields
from app.translations.translator import translator
from app.utils                   import receiver_subclasses
from django_countries.fields     import CountryField
from django.core.exceptions      import ValidationError
from django.db.models.signals    import post_save
from django.test                 import TestCase

from django.contrib.auth import get_user_model
User = get_user_model()

from random import randint

@receiver_subclasses(post_save, BaseQuestion, "basequestion_post_save")
@receiver_subclasses(post_save, BaseFeedback, "basefeedback_post_save")
def create_generic_element(sender, **kwargs):
    instance = kwargs.get('instance', None)
    if not kwargs.get('raw', False):
        ctype = ContentType.objects.get_for_model(instance)
        try:
            element = ThematicElement.objects.get(content_type=ctype, object_id=instance.pk)
        except ThematicElement.DoesNotExist:
            element = ThematicElement(content_object=instance)

        element.content_type = instance.content_type
        element.save()


@receiver_subclasses(post_save, ThematicElement, "thematicelement_post_save")
def create_thematic_element(sender, **kwargs):
    instance = kwargs.get('instance', None)
    try:
        filters  = dict(content_type=instance.content_type, object_id=instance.object_id)
        excludes = dict(id=instance.id)

        te       = ThematicElement.objects.filter(**filters).exclude(**excludes)

        # Remove this instance if the thematic element is already        
        if len(te):
            prev_el = te[0]
            if prev_el.thematic and not instance.thematic:
                instance.delete()
            else:
                prev_el.delete()
    except ThematicElement.DoesNotExist:
        pass


class CoreTestCase(TestCase):
    def setUp(self):
        post_save.connect(create_boolean_choices, sender=BooleanQuestion)
        post_save.connect(create_user_choice_fields, sender=UserGenderQuestion)

        # create user
        self.user = User.objects.create_user('myuser', 'myuser')
        # user question (country)
        self.user_question1 = UserCountryQuestion(label='l', hint_text='h', 
            profile_attribute='native_country' )
        self.user_question1.save()
        # user question (age)
        self.user_question2 = UserAgeQuestion(label='Age ?', hint_text='Nope')
        self.user_question2.save()

        # question 1 - text selection (1+ answer(s))
        self.question1 = TextSelectionQuestion(label='Question1 ?', hint_text='Chose one answer')
        self.question1.save()
        self.question1_choices = (
            TextChoiceField(title='choice1', question=self.question1, position=1),
            TextChoiceField(title='choice2', question=self.question1, position=2),
            TextChoiceField(title='choice3', question=self.question1, position=3),
        )
        [c.save() for c in self.question1_choices]

        # question 2 - text radio (1 answer)
        self.question2 = TextRadioQuestion(label='Question2 ?', hint_text='Chose one answer')
        self.question2.save()
        self.question2_choices = (
            TextChoiceField(title='choice1', question=self.question2, position=1),
            TextChoiceField(title='choice2', question=self.question2, position=2),
            TextChoiceField(title='choice3', question=self.question2, position=3),
        )
        [c.save() for c in self.question2_choices]

        # question 3 - typed number question 
        self.question3 = TypedNumberQuestion(
            label='Your weight ?', hint_text='Enter a date', unit='kg',
            min_number=0, max_number=200)

        self.question3.save()

        # feedback 1 - a static feedback to be embed in a thematic 
        self.feedback1 = StaticFeedback.objects.create(html_sentence="Feedback1", 
                source_url='http://jplusplus.org', source_title='jpp', 
                picture='')
        self.feedback1.save()

    def test_create_question(self):
        question = TypedNumberQuestion.objects.create(label='label', hint_text='hint', unit='%')
        question.save()

        ctype = ContentType.objects.get_for_model(question)
        thematic_element = ThematicElement.objects.filter(content_type=ctype, object_id=question.pk)
        self.assertEqual(len(thematic_element), 1)

    def test_create_answer_from_its_question(self):
        answer = self.question1.create_answer(user=self.user, value=(self.question1_choices[0]))
        answer.save()
        self.assertIsNotNone(answer)

    # Test that answering a user question change the answerer profile
    def test_answer_user_question_country(self): 
        country      = 'FR' # france country
        answer       = BaseAnswer.objects.create_answer(self.user_question1, self.user, country)
        answer_field = self.user_question1.profile_attribute
        answer.save()
        user_profile = UserProfile.objects.get(user_id=self.user)

        self.assertIsNotNone(answer)
        self.assertEqual(getattr(user_profile, answer_field).code, country)

    def test_answer_user_question_age(self):
        # check if AnswerManager's `create_answer` has the expected behavior
        age = 20 
        user_profile = UserProfile.objects.get(user_id=self.user)
        user_profile.age = 30
        user_profile.save()
        answer = BaseAnswer.objects.create_answer(self.user_question2, self.user, age)
        answer.save()
        # get latest object and check age is set to correct value
        user_profile = UserProfile.objects.get(user_id=self.user)
        self.assertEqual(user_profile.age, age)

    def test_create_user_gender_question(self): 
        question = UserGenderQuestion.objects.create(label='What is your gender?',
            hint_text='help')
        question.save()
        choices = UserChoiceField.objects.filter(question=question)
        self.assertEqual(len(choices), 2)
        self.assertIsNotNone(choices.filter(value='male')[0])
        self.assertIsNotNone(choices.filter(value='female')[0])

    def test_answer_user_gender_question(self):
        question = UserGenderQuestion.objects.create(label='What is your gender?',
            hint_text='help')
        question.save()
        choices = UserChoiceField.objects.filter(question=question)
        answer = question.create_answer(value=choices.filter(value='male')[0],
            user=self.user)
        answer.save()
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.gender, 'male')

    def test_answer_selection_question(self):
        question = self.question1
        choices  = self.question1_choices[:2]
        answer   = BaseAnswer.objects.create_answer(question, self.user, choices)
        answer.save()
        answered_choices = answer.value.all()

        # `find_modelinstance` function will lookup for current `choice` in 
        # answered choices to check every answered choices have been recorded
        map(lambda choice: 
                self.assertIsNotNone(
                    utils.find_modelinstance(choice, answered_choices)
                ) 
            , choices)

    def test_answer_radio_question(self):
        question = self.question2
        choices  = self.question2_choices
        value    = choices[0]
        answer   = BaseAnswer.objects.create_answer(question, self.user, value)
        answer.save()
        self.assertEqual(value, answer.value)


    def test_answer_typednumber_question(self):
        # TODO
        value    = 20
        question = self.question3
        answer   = BaseAnswer.objects.create_answer(question, self.user, value)
        answer.save()
        self.assertEqual(value, answer.value)

    def test_answer_typednumber_question_outofrange(self):
        value    = 300 
        question = self.question3
        failed   = False
        try:
            answer = BaseAnswer.objects.create_answer(question, self.user, value)
            answer.clean()
            answer.save()
        except ValidationError:
            failed = True
        self.assertTrue(failed)


    def test_multiple_answer(self): 
        # test that we can't create more than one answer on a given question
        iterations = 0
        question   = self.question3
        while iterations < 20:
            value = 100
            answer = BaseAnswer.objects.create_answer(question, self.user, value)
            answer.save()
            iterations += 1 

        answers = BaseQuestion.objects.get(pk=self.question3.id).baseanswer_set.all()
        self.assertEqual(len(answers), 1)


    def test_create_boolean_question(self):
        question = BooleanQuestion.objects.create(label='bool question', hint_text='answer by yes or no' )
        choices = TextChoiceField.objects.filter(question=question.pk)
        
        # check all choices are yes or no
        self.assertEqual(len(choices), 2)
        self.assertIsNotNone(choices.filter(title='yes')[0])
        self.assertIsNotNone(choices.filter(title='no')[0])

    def test_special_characters_question(self):
        question = BooleanQuestion.objects.create(label=u'é_è - ò_ó', hint_text=u'é_è')
        question.save()
        self.assertIsNotNone(question.__unicode__())


    def test_create_thematic(self):
        thematic = Thematic.objects.create(title='You')
        self.question1.set_thematic(thematic)
        self.question2.set_thematic(thematic)
        self.question3.set_thematic(thematic)
        self.assertEqual(len(thematic.thematicelement_set.all()), 3)


    def test_create_feedback(self):
        html_sentence = """
        Did you knew that we had <strong>6</strong> people working at 
        Journalism++ ? #RDP©
        """
        kwargs = {
            'html_sentence': html_sentence,
            'source_url': "http://jplusplus.org",
            'source_title': "jplusplus website"
        }
        feedback = StaticFeedback.objects.create(**kwargs)
        self.assertIsNotNone(feedback.as_element())

    def test_generic_thematic_elements(self):
        html_sentence = """
        Did you knew that we had <strong>6</strong> people working at 
        Journalism++ ? #RDP©
        """ 
        kwargs = {
            'html_sentence': html_sentence,
            'source_url': "http://jplusplus.org",
            'source_url': "jplusplus website"
        }
        feedback = StaticFeedback.objects.create(**kwargs)
        thematic = Thematic.objects.create(title='Your work')
        feedback.set_thematic(thematic)
        self.question1.set_thematic(thematic)
        self.assertEqual(len(thematic.thematicelement_set.all()), 2)


    def test_thematic_all_elements(self):
        thematic = Thematic.objects.create(title='Random title is random')
        thematic.save()

        thematic.add_element(self.question1, 1)
        thematic.add_element(self.question2, 2)
        thematic.add_element(self.feedback1, 3)
        thematic.save()
        elements = thematic.all_elements()

        self.assertEqual(len(elements), 3)
        self.assertEqual(elements[0].pk, self.question1.pk)
        self.assertIsNotNone(elements[0].label)

        self.assertEqual(elements[1].label, self.question2.label)
        self.assertIsNotNone(elements[1].label)

        self.assertEqual(elements[2].pk, self.feedback1.pk)
        self.assertIsNotNone(elements[2].source_url)


    def test_question_typologies(self):

        user_age_question        = UserAgeQuestion.objects.create(label='label', hint_text='hint')
        user_gender_question     = UserGenderQuestion.objects.create(label='label', hint_text='hint')
        user_country_question    = UserCountryQuestion.objects.create(label='label', hint_text='hint')
        text_selection_question  = TextSelectionQuestion.objects.create(label='label', hint_text='hint')
        media_selection_question = MediaSelectionQuestion.objects.create(label='label', hint_text='hint')
        text_radio_question      = TextRadioQuestion.objects.create(label='label', hint_text='hint')
        media_radio_question     = MediaRadioQuestion.objects.create(label='label', hint_text='hint')

        self.assertEqual( user_age_question.typology,         'user_age')
        self.assertEqual( user_gender_question.typology,      'user_gender')
        self.assertEqual( user_country_question.typology,     'user_country')
        self.assertEqual( text_selection_question.typology,   'text_selection')
        self.assertEqual( media_selection_question.typology,  'media_selection')
        self.assertEqual( text_radio_question.typology,       'text_radio')
        self.assertEqual( media_radio_question.typology,      'media_radio')

class ResultsTestCase(TestCase, utils.TestCaseMixin):
    def setUp(self):
        post_save.connect(create_boolean_choices, sender=BooleanQuestion)
        post_save.connect(create_user_choice_fields, sender=UserGenderQuestion)

        self.users = []
        self.answers = {}

        self.question1 = TypedNumberQuestion.objects.create(label='label', hint_text='hint')
        self.add_answer( self.question1, 15)
        self.add_answer( self.question1, 18)
        self.add_answer( self.question1, 19)
        self.add_answer( self.question1, 20)
        self.add_answer( self.question1, 21)
        self.add_answer( self.question1, 45)
        self.add_answer( self.question1, 45)
        self.add_answer( self.question1, 45)
        self.add_answer( self.question1, 70)
        self.add_answer( self.question1, 75)

        self.question2 = MediaSelectionQuestion.objects.create(label='label', hint_text='hint')
        self.question2_choices = (
            TextChoiceField.objects.create(title='choice1', question=self.question2, position=1),
            TextChoiceField.objects.create(title='choice2', question=self.question2, position=2),
            TextChoiceField.objects.create(title='choice3', question=self.question2, position=3),
        )
        self.question3 = BooleanQuestion.objects.create(label='label', hint_text='hint')
        
        for i in range(0,30):
            user = User.objects.create()
            profile = user.userprofile 
            profile.gender = GENDER_TYPES[randint(0,1)]
            profile.age = randint(0, 99)
            profile.save()
            self.users.append(user)

        call_selection_value = lambda q: q.choices()[randint(0, q.choices().count() - 1)]

        self.create_answers(self.question2, call_selection_value)
        self.create_answers(self.question3, call_selection_value)

        self.question4 = TypedNumberQuestion.objects.create(label='label', hint_text='hint')

    def create_dynfeedback(self, percentage=None, create_user_answer=True, user=None, question=None, value=None, 
                           other_value=None, nb_similar=502, nb_other=500):
        if create_user_answer:
            self.add_answer(question=question, user=user, value=value)
        for i in range(0, nb_similar): 
            self.add_answer(question=question, value=value,       copy_profile=user.userprofile)
        for i in range(0, nb_other):
            self.add_answer(question=question, value=other_value, copy_profile=user.userprofile)

        return transport.DynamicFeedback(use_percentage=percentage, user=user, question=question)


    def add_answer(self, question, value, user=None, copy_profile=None):
        if user == None:
            user = User.objects.create()

        if copy_profile != None:
            profile = user.userprofile
            for attr in ('age', 'gender', 'living_country', 'native_country'):
                setattr(profile, attr, getattr(copy_profile, attr, None))
            profile.save()
        self.answers[question.id] = question.create_answer(user=user, value=value)

    def create_answers(self, question, call_value):
        self.answers[question.id] = []
        for user in self.users:
            self.answers[question.id] = question.create_answer(
                value=call_value(question), 
                user=user
            )

    def check_results(self, results):
        results_dict = results.as_dict()
        self.assertIsNotNone(results)
        self.assertIsNotNone(results_dict)
        self.assertTrue(isinstance(results_dict, dict))
        self.assertAttrNotNone(results, 'sets')
        self.assertAttrNotNone(results_dict, 'sets')
        self.assertAttrNotNone(results, 'results')
        self.assertAttrNotNone(results_dict, 'results')

    def test_typed_number_question_results(self):
        results = self.question1.results()
        self.check_results(results)
        self.assertEqual(results.chart_type, 'histogramme')
        self.assertIsInstance(results, transport.Histogramme)

        sets = results.sets
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

        results = results.results 

        self.assertEqual( results[1], 30 )
        self.assertEqual( results[2], 20 )
        self.assertEqual( results[3], 30 )
        self.assertEqual( results[4], 20 )
        self.assertEqual( results[5], 0  )


    def test_selection_question_results(self):
        results = self.question2.results()
        self.assertIsInstance(results, transport.HorizontalBarChart)
        self.assertEqual(results.chart_type, 'horizontal_bar')
        self.check_results(results)
        total_percentage = 0 
        for (key,value) in results.results.items():
            total_percentage += value
        self.assertTrue(total_percentage <= 100)  

    def test_boolean_question_results(self):
        results = self.question3.results()
        self.assertIsInstance(results, transport.PieChart)
        self.assertEqual(results.chart_type, 'pie')

    def test_feedback_no_profile_attrs_no_percentage(self):
        # use case: user has filled no profile attribute (skipped all user 
        # questions 
        user = User.objects.create()
        feedback = self.create_dynfeedback(user=user, 
                                        percentage=False,
                                        question=self.question4,
                                        value=20, other_value=40)
        self.assertEqual(feedback.html_sentence, u"<strong>502</strong> persons answered like you")

    def test_feedback_no_profile_attrs_percentage(self):
        # use case: user has filled no profile attribute (skipped all user 
        # questions 
        user = User.objects.create()
        feedback = self.create_dynfeedback(
                                        percentage=True,
                                        user=user, 
                                        question=self.question4,
                                        value=20, other_value=40)
        self.assertEqual(feedback.html_sentence, u"<strong>50%</strong> of persons answered like you")

    def test_feedback_no_answer(self):
        user = User.objects.create()
        feedback = self.create_dynfeedback(create_user_answer=False,
                                           user=user, 
                                           question=self.question4,
                                           value=20, other_value=40)
        accepted_sentence = u'Until this day <strong>1002</strong> persons answered this question'
        self.assertEqual(feedback.html_sentence, accepted_sentence)


    def test_feedback_gender_with_percentage(self):
        user = User.objects.create()
        user.userprofile.gender = 'female'
        user.userprofile.save()
        feedback = self.create_dynfeedback(user=user,
                                           percentage=True, 
                                           question=self.question4,
                                           value=20, other_value=40)

        self.assertEqual(feedback.html_sentence, 
            u"<strong>50%</strong> of the females answered like you",)

    def test_feedback_gender_with_count(self):
        user = User.objects.create()
        user.userprofile.gender = 'male'
        user.userprofile.save()
        feedback = self.create_dynfeedback(user=user,
                                           percentage=False, 
                                           question=self.question4,
                                           value=20, other_value=40)

        self.assertEqual(feedback.html_sentence, 
            u"<strong>502</strong> males answered like you")



    def test_feedback_age_with_percentage(self):
        user = User.objects.create()
        user.userprofile.age = 27
        user.userprofile.save()
        feedback = self.create_dynfeedback(user=user,
                                           percentage=True, 
                                           question=self.question4,
                                           value=20, other_value=40)

        self.assertEqual(feedback.html_sentence, 
            u"<strong>50%</strong> of persons aged 27 years answered like you",)

    def test_feedback_age_with_count(self):
        user = User.objects.create()
        user.userprofile.age = 27
        user.userprofile.save()
        feedback = self.create_dynfeedback(user=user,
                                           percentage=False, 
                                           question=self.question4,
                                           value=20, other_value=40)

        self.assertEqual(feedback.html_sentence, 
            u"<strong>502</strong> persons aged 27 years answered like you")


    def test_feedback_living_country_count(self):
        user = User.objects.create()
        user.userprofile.living_country = 'FR'
        user.userprofile.save()
        feedback = self.create_dynfeedback(user=user,
                                           percentage=False, 
                                           question=self.question4,
                                           value=20, other_value=40)

        self.assertEqual(feedback.html_sentence, 
            u"<strong>502</strong> persons living in France answered like you")

    def test_feedback_living_country_percentage(self):
        user = User.objects.create()
        user.userprofile.living_country = 'FR'
        user.userprofile.save()
        feedback = self.create_dynfeedback(user=user,
                                           percentage=True, 
                                           question=self.question4,
                                           value=20, other_value=40)

        self.assertEqual(feedback.html_sentence, 
            u"<strong>50%</strong> of persons living in France answered like you")

    def test_feedback_native_country_count(self):
        user = User.objects.create()
        user.userprofile.native_country = 'FR'
        user.userprofile.save()
        feedback = self.create_dynfeedback(user=user,
                                           percentage=False, 
                                           question=self.question4,
                                           value=20, other_value=40)

        self.assertEqual(feedback.html_sentence, 
            u"<strong>502</strong> persons from France answered like you")

    def test_feedback_native_country_percentage(self):
        user = User.objects.create()
        user.userprofile.native_country = 'FR'
        user.userprofile.save()
        feedback = self.create_dynfeedback(user=user,
                                           percentage=True, 
                                           question=self.question4,
                                           value=20, other_value=40)

        self.assertEqual(feedback.html_sentence, 
            u"<strong>50%</strong> of persons from France answered like you")

class UtilsTestCase(TestCase, utils.TestCaseMixin):

    def test_fileexists(self):
        self.assertTrue( utils.fileexists('.'))
        self.assertFalse(utils.fileexists('I_DO_NOT_EXISTS.such.file'))

    def test_get_field_names(self):
        # unit test for utils.get_fields_names function
        names = utils.get_fields_names(UserProfile, CountryField)
        self.assertTrue(UserProfile._meta.get_field('native_country').name in names)
        self.assertTrue(UserProfile._meta.get_field('living_country').name in names)

    def test_camel_to_underscore(self):
        self.assertEqual(utils.camel_to_underscore("CamelCaseToUnderscore"), "camel_case_to_underscore")

    def test_without(self):
        arr = ('a', 'b', 'c')
        self.assertEqual(utils.without(arr, 'b'), ('a', 'c'))

    def test_om_getattr_dict(self):
        element = {
            'one': 1,
            'none': None
        }
        self.assertEqual(utils.om_getattr(element, 'one'),  element['one'])
        self.assertEqual(utils.om_getattr(element, 'none'), element['none'])

    def test_om_getattr_object(self):
        class Test:
            def __init__(self):
                self.one = 1
                self.none = None

        element = Test()
        self.assertEqual(utils.om_getattr(element, 'one'),  element.one)
        self.assertEqual(utils.om_getattr(element, 'none'), element.none)

    def test_find_where_simple(self):
        arr = (
            {'id': 0, 'name':'0'},
            {'id': 1, 'name':'1'},
            {'id': 2, 'name':'2'}
        )
        res = utils.find_where(arr, {'id': 0})
        self.assertIsNotNone(res)
        self.assertEqual(res['name'], '0')

    def test_find_where_multiple(self):
        arr = (
            {'id': 0, 'name':'1', 'other': 2 },
            {'id': 1, 'name':'1', 'other': 5 }, 
            {'id': 2, 'name':'2', 'other': 7 }
        )
        res = utils.find_where(arr, {'name': '1', 'id': 1})
        self.assertIsNotNone(res)
        self.assertEqual(res['other'], 5)

    def test_assert_attr_not_none_dict(self):
        test_element = {
            'not_none_attr': 'not None',
            'none_attr': None
        }
        with self.assertRaises(AssertionError):
            self.assertAttrNotNone(test_element, 'none_attr')
        with self.assertRaises(AssertionError): 
            self.assertAttrNotNone(test_element, 'not_existing')

        try:
            self.assertAttrNotNone(test_element, 'not_none_attr')
        except AssertionError as e:
            self.fail( 'assertAttrNotNone raised an error: {e}'.format(e=e))

    def test_assert_attr_not_none_object(self):
        class Test:
            def __init__(self):
                self.not_none_attr = 'not none'
                self.none_attr = None

        test_element = Test()

        with self.assertRaises(AssertionError):
            self.assertAttrNotNone(test_element, 'none_attr')
        with self.assertRaises(AssertionError): 
            self.assertAttrNotNone(test_element, 'not_existing')

        try:
            self.assertAttrNotNone(test_element, 'not_none_attr')
        except AssertionError as e:
            self.fail( 'assertAttrNotNone failed where it shouldn\'t: {e}'.format(e=e))


    def test_assert_attr_equal_obj(self):
        class Test:
            def __init__(self):
                self.one = 1
                self.none = None

        test_element = Test()

        with self.assertRaises(AssertionError):
            self.assertAttrEqual(test_element, 'one', 2)
        try:
            self.assertAttrEqual(test_element, 'one', 1)
            self.assertAttrEqual(test_element, 'none', None)
        except AssertionError as e:
            self.fail( 'assertAttrEqual failed where it shouldn\'t: {e}'.format(e=e))


class ModelTranslationTestCase(TestCase, utils.TestCaseMixin):
    def test_question_opts(self):
        opts = translator.get_options_for_model(BaseQuestion)
        fields = opts.fields
        self.assertAttrNotNone(fields, 'label')
        self.assertAttrNotNone(fields, 'hint_text')
        self.assertAttrNotNone(fields, 'skip_button_label')