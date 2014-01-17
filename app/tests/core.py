# all core related tests should go here
from app.auth.models             import UserProfile
from app.core.models             import BaseAnswer, UserCountryQuestion
from django.contrib.auth.models  import User
from django.test                 import TestCase
from django_countries.fields     import CountryField

class CoreTestCase(TestCase):
    def setUp(self):
        # create user
        self.user = User.objects.create()
        self.user_question1 = UserCountryQuestion(label='l', hint_text='h')
        # create user question

    def test_user_question(self): 
        country      = CountryField('FR') # france country
        answer       = BaseAnswer.objects.create_answer(self.user_question1, self.user, country)
        user_profile = UserProfile.objects.get(user=self.user)

        self.assertNotNone(answer)
        self.assertEqual(user_profile.country, country)
