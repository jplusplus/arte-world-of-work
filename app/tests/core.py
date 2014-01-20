# all core related tests should go here
from app                         import utils   
from app.core.models             import BaseAnswer, UserCountryQuestion, UserProfile
from app.core.models             import DateQuestion, TypedNumberQuestion
from app.core.models             import TextSelectionQuestion, TextRadioQuestion
from app.core.models             import UserAgeQuestion, TextChoiceField
from app.core.models             import BaseQuestion
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

        # question 3 - date question 
        self.question3 = DateQuestion(label='Date ?', hint_text='Enter a date')
        self.question3.save()        

        # question 4 - typed number question 
        self.question4 = TypedNumberQuestion(
            label='Your weight ?', hint_text='Enter a date', unit='kg',
            min_number=0, max_number=200)

        self.question4.save()

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
        from datetime import datetime
        value = datetime.now()
        question = self.question3 
        answer = BaseAnswer.objects.create_answer(question, self.user, value)
        answer.save()
        self.assertEqual(value, answer.value)


    def test_answer_typednumber_question(self):
        # TODO
        value = 20
        question = self.question4
        answer = BaseAnswer.objects.create_answer(question, self.user, value)
        answer.save()
        self.assertEqual(value, answer.value)

    def test_answer_typednumber_question_outofrange(self):
        value = 300 
        question = self.question4
        failed = False
        try:
            answer = BaseAnswer.objects.create_answer(question, self.user, value)
            answer.clean()
            answer.save()
        except ValidationError:
            failed = True

        self.assertTrue(failed)


    def test_multiple_answer(self): 
        # test that we can actually create multiple answer for a given question 
        iteration = 0
        question = self.question4
        while iteration < 20:
            value = 100
            answer = BaseAnswer.objects.create_answer(question, self.user, value)
            answer.save()
            iteration += 1 


        answers = BaseQuestion.objects.get(pk=self.question4.id).baseanswer_set.all()
        self.assertEqual(len(answers), iteration)
