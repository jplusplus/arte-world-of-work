# all core related tests should go here
from app                         import utils   
from app.core.models             import BaseAnswer, UserCountryQuestion, UserProfile
from app.core.models             import UserAgeQuestion, TextChoiceField
from app.core.models             import TextSelectionQuestion, TextRadioQuestion
from django.contrib.auth.models  import User
from django.test                 import TestCase


class CoreTestCase(TestCase):

    def setUp(self):
        # create user
        self.user = User.objects.create()
        UserProfile.objects.create(user=self.user)
        self.user_question1 = UserCountryQuestion(label='l', hint_text='h')
        self.user_question1.save()
        self.user_question2 = UserAgeQuestion(label='Age ?', hint_text='Nope')
        self.user_question2.save()

        self.question1 = TextSelectionQuestion(label='Choices ?', hint_text='Chose one answer')
        self.question1.save()
        self.question1_choices = (
            TextChoiceField(title='choice1', question=self.question1),
            TextChoiceField(title='choice2', question=self.question1),
            TextChoiceField(title='choice3', question=self.question1),
        )
        [c.save() for c in self.question1_choices]
        self.question2 = TextRadioQuestion(label='Choices ?', hint_text='Chose one answer')
        self.question2.save()
        self.question2_choices = (
            TextChoiceField(title='choice1', question=self.question2),
            TextChoiceField(title='choice2', question=self.question2),
            TextChoiceField(title='choice3', question=self.question2),
        )
        [c.save() for c in self.question2_choices]




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
        assertion = lambda c: self.assertIsNotNone(utils.find_modelinstance(c,answer.value.all()))
        map(assertion, choices)


    def test_answer_radio_question(self):
        question = self.question2
        choices  = self.question2_choices
        value    = choices[0]
        answer   = BaseAnswer.objects.create_answer(question, self.user, value)
        answer.save()
        self.assertEqual(value, answer.value)

    def test_answer_date_question(self):
        # TODO
        code_me = 'PLEASE'
        # value = 

    def test_answer_number_question(self):
        # TODO
        code_me = 'PLEASE'
