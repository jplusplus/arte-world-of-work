# all core related tests should go here
from app.core.models             import BaseAnswer, UserCountryQuestion, UserProfile
from django.contrib.auth.models  import User
from django.test                 import TestCase

class CoreTestCase(TestCase):
    def setUp(self):
        # create user
        self.user = User.objects.create()
        UserProfile.objects.create(user=self.user)
        self.user_question1 = UserCountryQuestion(label='l', hint_text='h')
        self.user_question1.save()
        # create user question

    def test_user_question(self): 
        country      = 'FR' # france country
        answer       = BaseAnswer.objects.create_answer(self.user_question1, self.user, country)
        answer.save()
        user_profile = UserProfile.objects.get(user_id=self.user)

        self.assertIsNotNone(answer)
        self.assertEqual(user_profile.country.code, country)
