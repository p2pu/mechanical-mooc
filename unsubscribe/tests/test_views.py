"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client

from mock import patch
import math

from signup import models as signup_models

@patch('signup.models.sequence_model.get_current_sequence_number', lambda: 1)
class ViewTest(TestCase):

    SIGNUP_DATA = {
        'email': 'dirk@mail.com',
        'questions': {'q1':'a1', 'q2':'a2', 'q3':'a3'}
    }


    @patch('unsubscribe.emails.mailgun.api.send_email')
    def test_unsubscribe(self, *args, **kwargs):
        signup_models.create_signup(**self.SIGNUP_DATA)
        c = Client()
        resp = c.post('/unsubscribe/', self.SIGNUP_DATA)
        self.assertRedirects(resp, '/')
        self.assertTrue(args[0].called)


    @patch('unsubscribe.emails.mailgun.api.send_email')
    def test_non_signed_up_unsubscribe(self, *args, **kwargs):
        c = Client()
        resp = c.post('/unsubscribe/', self.SIGNUP_DATA)
        self.assertFalse(args[0].called)
    

    @patch('unsubscribe.views.unsubscribe_model.unsubscribe_user')
    def test_unsubscribe_confirm(self, *args, **kwargs):
        su = signup_models.create_signup(**self.SIGNUP_DATA)
        c = Client()
        resp = c.post('/unsubscribe/confirm/{0}/'.format(su['key']), self.SIGNUP_DATA)
        self.assertRedirects(resp, '/')
        self.assertTrue(args[0].called)

    
    @patch('unsubscribe.views.unsubscribe_model.unsubscribe_user')
    def test_unsubscribe_confirm_error(self, *args, **kwargs):
        su = signup_models.create_signup(**self.SIGNUP_DATA)
        c = Client()
        resp = c.post('/unsubscribe/confirm/{0}cc/'.format(su['key']), self.SIGNUP_DATA)
        self.assertFalse(args[0].called)
