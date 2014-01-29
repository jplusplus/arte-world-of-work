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
from django.contrib.auth.models  import User
from django.core.exceptions      import ValidationError
from django.test                 import TestCase


class CoreTestCase(TestCase):
    def setUp(self):
        # create user
        self.user = User.objects.create()
        UserProfile.objects.create(user=self.user)
        # user question (country)
        self.user_question1 = UserCountryQuestion(label='l', hint_text='h')
        self.user_question1.save()
        # user question (age)
        self.user_question2 = UserAgeQuestion(label='Age ?', hint_text='Nope')
        self.user_question2.save()

        # question 1 - text selection (1+ answer(s))
        self.question1 = TextSelectionQuestion(label='Choices ?', hint_text='Chose one answer')
        self.question1.save()
        self.question1_choices = (
            TextChoiceField(title='choice1', question=self.question1),
            TextChoiceField(title='choice2', question=self.question1),
            TextChoiceField(title='choice3', question=self.question1),
        )
        [c.save() for c in self.question1_choices]

        # question 2 - text radio (1 answer)
        self.question2 = TextRadioQuestion(label='Choices ?', hint_text='Chose one answer')
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

    def test_create_question(self):
        question = NumberQuestion.objects.create(label='label', hint_text='hint')
        question.save()

        ctype = ContentType.objects.get_for_model(question)
        thematic_element = ThematicElement.objects.filter(content_type=ctype, object_id=question.pk)
        self.assertEqual(len(thematic_element), 1)


    # Test that answering a user question change the answerer profile
    def test_answer_user_question_country(self): 
        country      = 'FR' # france country
        answer       = BaseAnswer.objects.create_answer(self.user_question1, self.user, country)
        answer.save()
        user_profile = UserProfile.objects.get(user_id=self.user)

        self.assertIsNotNone(answer)
        self.assertEqual(user_profile.country.code, country)


    def test_answer_user_question_age(self):
        age = 20 
        user_profile = UserProfile.objects.get(user_id=self.user)
        user_profile.age = 30
        user_profile.save()
        answer = BaseAnswer.objects.create_answer(self.user_question2, self.user, age)
        answer.save()
        # get latest object
        user_profile = UserProfile.objects.get(user_id=self.user)
        self.assertEqual(user_profile.age, age)

    def test_answer_selection_question(self):
        question = self.question1
        choices  = self.question1_choices[:2]
        answer   = BaseAnswer.objects.create_answer(question, self.user, choices)
        answer.save()
        answered_choices = answer.value.all()
        # assert for every choice that 
        map(lambda choice: 
                # utils.find_modelinstance function will lookup for current `choice` in
                # answered choices and check if the result is not None (=> exists)
                self.assertIsNotNone(utils.find_modelinstance(choice, answered_choices)) 
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
        self.assertEqual(len(answers), iteration)


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
