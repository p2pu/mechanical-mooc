"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from mock import patch

from unsubscribe import models as unsubscribe_model

@patch('unsubscribe.models.mailgun_api.remove_list_member')
@patch('unsubscribe.models.mailgun_api.delete_all_unsubscribes')
@patch('unsubscribe.models.signup_model.remove_signup_from_sequence')
@patch('unsubscribe.models.signup_model.delete_signup')
@patch('unsubscribe.models.signup_model.get_signup', lambda x: {'sequence': 1})
class SimpleTest(TestCase):

    def test_unsubscribe_user(self, *args):
        unsubscribe_model.unsubscribe_user('user@mail.com')

    
    def test_unsibscribe_user_from_sequence(self, *args):
        unsubscribe_model.unsubscribe_from_sequence('user@mail.com')

