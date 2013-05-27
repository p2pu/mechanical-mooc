from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from mock import patch
import math
import datetime


class ViewTest(TestCase):

    SIGNUP_DATA = {
        'email': 'dirk@mail.com',
        'timezone': 'Africa/Johannesburg',
        'groupRadios': 'true', 
        'styleRadios': 'try', 
        'expertiseRadios': 'think',
        'csrfmiddlewaretoken': '123'
    }


    def setUp(self):
        user = User.objects.create_user('admin', 'admin@test.com', 'password')


    def test_login_required(self):
        urls = [
            '/mail/compose/',
            '/mail/send_preview/',
            '/mail/schedule/'
        ]
        c = Client()
        resp = c.get('/mail/schedule/')
        self.assertRedirects(resp, '/accounts/login/?next=/mail/schedule/')


    def test_schedule_view(self):
        c = Client()
        self.assertTrue(c.login(username='admin', password='password'))
        resp = c.get('/mail/schedule/')
        self.assertEquals(resp.status_code, 200)


    @patch('mail.models.schedule_email')
    def test_schedule(self, *args):
        now = datetime.datetime.utcnow()
        future = now + datetime.timedelta(days=1)
        past = now - datetime.timedelta(hours=1)
        c = Client()
        self.assertTrue(c.login(username='admin', password='password'))
        post_data = {
            'scheduled_date': future.strftime('%Y-%m-%d'),
            'scheduled_time': future.strftime('%H:%M')
        }
        resp = c.post('/mail/schedule_email/1/', post_data)
        self.assertEquals(resp.status_code, 200)

        post_data = {
            'scheduled_date': past.strftime('%Y-%m-%d'),
            'scheduled_time': past.strftime('%H:%M')
        }
        resp = c.post('/mail/schedule_email/1/', post_data)
        self.assertEquals(resp.status_code, 400)


    def test_compose(self):
        raise Exception()


    def test_edit(self):
        raise Exception()


    def test_delete(self):
        raise Exception()


    def test_send(self):
        raise Exception()


    @patch('mail.views.mailgun_api.send_email')
    def test_send_preview(self, *args):
        c = Client()
        self.assertTrue(c.login(username='admin', password='password'))
        post_data = {
            'subject': 'Test subject',
            'body_text': '<p>This is a test</p>',
            'test_email': 'test@mail.com'
        }
        resp = c.post('/mail/send_preview/', post_data)
        self.assertEquals(resp.status_code, 200)

