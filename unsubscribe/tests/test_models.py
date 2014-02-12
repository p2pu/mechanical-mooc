"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from mock import patch

from unsubscribe import models as unsubscribe_model
from signup import models as signup_model

@patch('signup.models.sequence_model.get_current_sequence_number', lambda: 1)
class SimpleTest(TestCase):

    @patch('unsubscribe.models.mailgun_api.remove_list_member')
    @patch('unsubscribe.models.mailgun_api.delete_all_unsubscribes')
    @patch('unsubscribe.models.signup_model.delete_signup')
    @patch('unsubscribe.models.signup_model.get_all_user_signups', lambda x: [{'sequence': 1}])
    def test_unsubscribe_user(self, *args):
        unsubscribe_model.unsubscribe_user('user@mail.com')
        self.assertTrue(args[0].called)
        self.assertTrue(args[1].called)
        self.assertTrue(args[2].called)


    @patch('unsubscribe.models.mailgun_api.remove_list_member')
    def test_unsubscribe_signup_up_user(self, remove_list_member):
        signup_model.create_signup('dirk@mail.com', {'q1':'a1', 'q2':'a2', 'q3':'a3'})
        unsubscribe_model.unsubscribe_user('dirk@mail.com')
        self.assertTrue(remove_list_member.called)
