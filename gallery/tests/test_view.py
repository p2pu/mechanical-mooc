from django.test import TestCase
from django.test.client import Client

from mock import patch

from signup import models as signup_api


@patch('signup.models.sequence_model.get_current_sequence_number', lambda: 1)
class ViewTest(TestCase):

    SIGNUP_DATA = {
        'email': 'user@mail.com',
        'questions': {
            'timezone': 'Africa/Johannesburg',
            'groupRadios': 'true', 
            'styleRadios': 'try', 
            'expertiseRadios': 'think',
        }
    }

    BIO_DATA = {
        'email': 'user@mail.com',
        'name': 'Test User',
        'bio': 'This is some info',
        'avatar': 'http://placehold.it/120x120'
    }

    def test_sequence_redirect(self):
        c = Client()
        resp = c.get('/gallery/')
        self.assertRedirects(resp, '/gallery/1/')
    
    
    def test_un_signedup_bio(self):
        c = Client()
        resp = c.post('/gallery/1/save_bio/', self.BIO_DATA)
        self.assertRedirects(resp, '/')

    @patch('gallery.views.send_confirmation_email')
    def test_signedup_bio(self, patcher):
        signup_api.create_signup(**self.SIGNUP_DATA)
        c = Client()
        resp = c.post('/gallery/1/save_bio/', self.BIO_DATA)
        self.assertRedirects(resp, '/gallery/1/')
