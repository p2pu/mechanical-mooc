"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from signup import models as signup_models
from signup import randata
from mock import patch
import math

@patch('signup.models.sequence_model.get_current_sequence_number', lambda: 1)
class SimpleTest(TestCase):

    def setUp(self):
        self.signup_data = [
            'dirk@mail.com',
            {'q1':'a1', 'q2':'a2', 'q3':'a3'}
        ]

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
        self.assertIn('date_created', signup)
        self.assertIn('date_updated', signup)


    def test_update_signup(self):
        original = signup_models.create_or_update_signup('dirk@mail.com', {'q1':'a1', 'q2':'a2', 'q3':'a3'})
        signup_models.create_or_update_signup('dirk@mail.com', {'q1':'ar1', 'q2':'ar2'})
        signup = signup_models.get_signup('dirk@mail.com')
        self.assertEqual(signup['email'], 'dirk@mail.com')
        self.assertEqual(signup['questions']['q1'], 'ar1')
        self.assertEqual(signup['questions']['q2'], 'ar2')
        self.assertEqual(signup['questions']['q3'], 'a3')
        self.assertEqual(original['date_created'], signup['date_created'])
        self.assertNotEqual(original['date_updated'], signup['date_updated'])


    def test_get_signups(self):
        signup_models.create_or_update_signup('user1@mail.com', {'q1':'a1', 'q2':'a2', 'q3':'a3'})
        signup_models.create_or_update_signup('user1@mail.com', {'q1':'ar1', 'q2':'ar2'})
        signup_models.create_or_update_signup('user2@mail.com', {'q1':'ar1', 'q2':'ar2'})
        signup_models.create_or_update_signup('user3@mail.com', {'q1':'ar1', 'q2':'ar2'})
        signup_models.create_or_update_signup('user4@mail.com', {'q1':'ar1', 'q2':'ar2'})

        self.assertEqual(len(signup_models.get_signups()), 4)


    def test_signup_added_without_sequence(self):
        with patch('signup.models.sequence_model.get_current_sequence_number', lambda: None):
            signup_models.create_or_update_signup(*self.signup_data)
        signup = signup_models.get_signup(self.signup_data[0])
        self.assertNotEqual(signup, None)


    def test_signup_added_to_current_sequence(self):
        signup_models.create_or_update_signup('dirk@mail.com', {'q1':'ar1', 'q2':'ar2'})
        signup = signup_models.get_signup('dirk@mail.com')
        self.assertEquals(signup['sequence'], 1)

        with patch('signup.models.sequence_model.get_current_sequence_number', lambda: 2):
            signup_models.create_or_update_signup('dirk@mail.com', {'q1':'ar1', 'q2':'ar2'})

        signup = signup_models.get_signup('dirk@mail.com')
        self.assertEquals(signup['sequence'], 2)


    def test_get_signups_for_sequence(self):
        signup_models.create_or_update_signup('user1@mail.com', {'q1':'a1', 'q2':'a2', 'q3':'a3'})
        signup_models.create_or_update_signup('user1@mail.com', {'q1':'ar1', 'q2':'ar2'})
        signup_models.create_or_update_signup('user2@mail.com', {'q1':'ar1', 'q2':'ar2'})
        signup_models.create_or_update_signup('user3@mail.com', {'q1':'ar1', 'q2':'ar2'})
        with patch('signup.models.sequence_model.get_current_sequence_number', lambda: 2):
            signup_models.create_or_update_signup('user3@mail.com', {'q1':'ar1'})
            signup_models.create_or_update_signup('user4@mail.com', {'q1':'ar1'})
            signup_models.create_or_update_signup('user5@mail.com', {'q1':'ar1'})
            signup_models.create_or_update_signup('user6@mail.com', {'q1':'ar1'})

        self.assertEqual(len(signup_models.get_signups(1)), 2)
        self.assertEqual(len(signup_models.get_signups(2)), 4)


    def test_welcome_email(self):
        signup_models.create_or_update_signup('user1@mail.com', {'q1':'a1', 'q2':'a2', 'q3':'a3'})
        self.assertEqual(len(signup_models.get_new_signups()), 1)

        with patch('signup.models.emails.send_welcome_emails') as send_email:
            signup_models.send_welcome_email('user1@mail.com')
            self.assertTrue(send_email.called)

        self.assertEqual(len(signup_models.get_new_signups()), 0)


    def test_scale_signups(self):
        for signup in randata.random_data(2000):
            signup_models.create_or_update_signup(**signup)

        signups = len(signup_models.get_new_signups())

        with patch('signup.models.emails.send_welcome_emails') as send_email:
            with patch('signup.models.mailgun_api.add_list_member') as add_list_member:
                with patch('signup.models.sequence_model.sequence_list_name', lambda x: 'sequence-2-all@test-domain.org'):
                    signup_models.handle_new_signups()
                    self.assertTrue(send_email.called)
                    self.assertEqual(send_email.call_count, math.ceil(signups/500.0))
                    self.assertTrue(add_list_member.called)
                    self.assertEqual(add_list_member.call_count, signups)

        self.assertEqual(len(signup_models.get_new_signups()), 0)


    def test_delete_signup(self):
        signup_models.create_or_update_signup('user1@mail.com', {'q1':'a1', 'q2':'a2', 'q3':'a3'})
        signup_models.create_or_update_signup('user1@mail.com', {'q1':'ar1', 'q2':'ar2'})
        signup_models.create_or_update_signup('user2@mail.com', {'q1':'ar1', 'q2':'ar2'})
        signup_models.create_or_update_signup('user3@mail.com', {'q1':'ar1', 'q2':'ar2'})
        signup_models.create_or_update_signup('user4@mail.com', {'q1':'ar1', 'q2':'ar2'})

        self.assertEqual(len(signup_models.get_signups()), 4)
        new_signups = signup_models.get_new_signups()
        self.assertIn('user3@mail.com', [s['email'] for s in new_signups])

        signup_models.delete_signup('user3@mail.com')

        signups = signup_models.get_signups()
        self.assertEqual(len(signups), 3)
        self.assertNotIn('user3@mail.com', [s['email'] for s in signups])
        new_signups = signup_models.get_new_signups()
        self.assertNotIn('user3@mail.com', [s['email'] for s in new_signups])

        signup_models.create_or_update_signup('user3@mail.com', {'q1':'ar1', 'q2':'ar2'})
        self.assertEqual(len(signup_models.get_signups()), 4)
        new_signups = signup_models.get_new_signups()
        self.assertIn('user3@mail.com', [s['email'] for s in new_signups])


    def test_remove_signup_from_sequence(self):
        signup_models.create_or_update_signup('dirk@mail.com', {'q1':'ar1', 'q2':'ar2'})
        signup = signup_models.get_signup('dirk@mail.com')
        self.assertEquals(signup['sequence'], 1)

        with patch('signup.models.sequence_model.get_current_sequence_number', lambda: 2):
            signup_models.remove_signup_from_sequence('dirk@mail.com')

        signup = signup_models.get_signup('dirk@mail.com')
        self.assertEquals(signup['sequence'], 2)

        signup_models.create_or_update_signup('user@mail.com', {'q1':'ar1', 'q2':'ar2'})
        signup = signup_models.get_signup('user@mail.com')
        self.assertEquals(signup['sequence'], 1)

        with patch('signup.models.sequence_model.get_current_sequence_number', lambda: None):
            signup_models.remove_signup_from_sequence('dirk@mail.com')

        signup = signup_models.get_signup('dirk@mail.com')
        self.assertEquals(signup['sequence'], None)

