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
from app.core.models             import * 
from app.utils                   import get_fields_names
from django_countries.fields     import CountryField
from django.contrib.auth.models  import User
from django.core.exceptions      import ValidationError
from django.test                 import TestCase

class CoreTestCase(TestCase):
    def setUp(self):
        # create user
        self.user = User.objects.create()
        UserProfile.objects.create(user=self.user)
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
            TextChoiceField(title='choice1', question=self.question1),
            TextChoiceField(title='choice2', question=self.question1),
            TextChoiceField(title='choice3', question=self.question1),
        )
        [c.save() for c in self.question1_choices]

        # question 2 - text radio (1 answer)
        self.question2 = TextRadioQuestion(label='Question2 ?', hint_text='Chose one answer')
        self.question2.save()
        self.question2_choices = (
            TextChoiceField(title='choice1', question=self.question2),
            TextChoiceField(title='choice2', question=self.question2),
            TextChoiceField(title='choice3', question=self.question2),
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

    def test_get_field_names(self):
        # unit test for utils.get_fields_names function
        names = get_fields_names(UserProfile, CountryField)
        self.assertTrue('native_country' in names)
        self.assertTrue('living_country' in names)

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
        # get latest object
        user_profile = UserProfile.objects.get(user_id=self.user)
        self.assertEqual(user_profile.age, age)

    def test_create_user_gender_question(self): 
        question = UserGenderQuestion.objects.create(label='What is your gender?',
            hint_text='help')
        question.save()
        # import pdb; pdb.set_trace()
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
        # test that we can actually create multiple answer for a given question 
        iterations = 0
        question   = self.question3
        while iterations < 20:
            value = 100
            answer = BaseAnswer.objects.create_answer(question, self.user, value)
            answer.save()
            iterations += 1 

        answers = BaseQuestion.objects.get(pk=self.question3.id).baseanswer_set.all()
        self.assertEqual(len(answers), iterations)


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





