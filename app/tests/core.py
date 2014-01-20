# all core related tests should go here
from app.core.models             import BaseAnswer, UserCountryQuestion, UserProfile
from app.core.models             import UserAgeQuestion
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
        # create user question

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

