"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from signup import models as signup_models

class SimpleTest(TestCase):
    def test_create_signup(self):
        """
        Test creation of a signup
        """
        signup_models.create_signup('dirk@mail.com', {'q1':'a1', 'q2':'a2', 'q3':'a3'})
        signup = signup_models.get_signup('dirk@mail.com')
        self.assertEqual(signup['email'], 'dirk@mail.com')
        self.assertEqual(signup['questions']['q1'], 'a1')
        self.assertEqual(signup['questions']['q2'], 'a2')
        self.assertEqual(signup['questions']['q3'], 'a3')
        self.assertTrue('date_created' in signup)
        self.assertTrue('date_updated' in signup)


    def test_update_signup(self):
        signup_models.create_or_update_signup('dirk@mail.com', {'q1':'a1', 'q2':'a2', 'q3':'a3'})
        signup_models.create_or_update_signup('dirk@mail.com', {'q1':'ar1', 'q2':'ar2'})
        signup = signup_models.get_signup('dirk@mail.com')
        self.assertEqual(signup['email'], 'dirk@mail.com')
        self.assertEqual(signup['questions']['q1'], 'ar1')
        self.assertEqual(signup['questions']['q2'], 'ar2')
        self.assertEqual(signup['questions']['q3'], 'a3')
        self.assertTrue('date_created' in signup)
        self.assertTrue('date_updated' in signup)


    def test_get_signups(self):
        signup_models.create_or_update_signup('user1@mail.com', {'q1':'a1', 'q2':'a2', 'q3':'a3'})
        signup_models.create_or_update_signup('user1@mail.com', {'q1':'ar1', 'q2':'ar2'})
        signup_models.create_or_update_signup('user2@mail.com', {'q1':'ar1', 'q2':'ar2'})
        signup_models.create_or_update_signup('user3@mail.com', {'q1':'ar1', 'q2':'ar2'})
        signup_models.create_or_update_signup('user4@mail.com', {'q1':'ar1', 'q2':'ar2'})

        self.assertEqual(len(signup_models.get_signups()), 4)

