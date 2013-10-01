from django.test import TestCase
from django.test.client import Client

from mock import patch


@patch('signup.models.sequence_model.get_current_sequence_number', lambda: 1)

class ViewTest(TestCase):

    SIGNUP_DATA = {
        'email': 'user@mail.com',
        'timezone': 'Africa/Johannesburg',
        'groupRadios': 'true', 
        'styleRadios': 'try', 
        'expertiseRadios': 'think',
    }

    BIO_DATA = {
        'email': 'user@mail.com',
    }

    def test_sequence_redirect(self):
        c = Client()
        resp = c.get('/gallery/')
        self.assertRedirects(resp, '/gallery/1/')
    
    
    def test_signup_view(self):
        c = Client()
        resp = c.post('/gallery/1/save_bio/', self.SIGNUP_DATA)
        self.assertRedirects(resp, '/success')

