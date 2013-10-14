from django.test import TestCase
from django.test.client import Client

from mock import patch

from signup import models as signup_api
from classphoto import models as classphoto_api

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
        resp = c.get('/classphoto/')
        self.assertRedirects(resp, '/classphoto/1/')
    
    
    def test_un_signedup_bio(self):
        c = Client()
        resp = c.post('/classphoto/1/save_bio/', self.BIO_DATA)
        self.assertRedirects(resp, '/classphoto/1/')
        bios = classphoto_api.get_bios(1)
        self.assertEquals(len(bios), 0)


    def test_signed_up_not_signed_in_bio_save(self):
        signup_api.create_signup(**self.SIGNUP_DATA)
        c = Client()
        resp = c.post('/classphoto/1/save_bio/', self.BIO_DATA)
        self.assertRedirects(resp, '/classphoto/1/')
        bios = classphoto_api.get_bios(1)
        self.assertEquals(len(bios), 0)


    @patch('classphoto.emails.mailgun.api.send_email')
    def test_request_user_link(self, patcher):
        signup = signup_api.create_signup(**self.SIGNUP_DATA)
        c = Client()
        resp = c.post('/classphoto/request_link/', self.BIO_DATA, follow=True)
        self.assertRedirects(resp, '/classphoto/1/')
        self.assertTrue(patcher.called)
    

    def test_signed_in(self):
        signup = signup_api.create_signup(**self.SIGNUP_DATA)
        c = Client()
        resp = c.get('/classphoto/1/?key={0}'.format(signup['key']))
        session = c.session
        self.assertEquals(session['user_email'], self.BIO_DATA['email'])
        self.assertRedirects(resp, '/classphoto/1/')
    

    def test_signed_up_signed_in_bio_save(self):
        signup = signup_api.create_signup(**self.SIGNUP_DATA)
        c = Client()
        resp = c.get('/classphoto/1/?key={0}'.format(signup['key']))
        resp = c.post('/classphoto/1/save_bio/', self.BIO_DATA)
        self.assertRedirects(resp, '/classphoto/1/')
        bios = classphoto_api.get_bios(0)
        self.assertEquals(len(bios), 0)
