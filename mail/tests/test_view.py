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
        c = Client()
        self.assertTrue(c.login(username='admin', password='password'))

        resp = c.get('/mail/compose/')
        self.assertEquals(resp.status_code, 200)

        post_data = {
            'subject': 'Test subject',
            'body_text': '<p>This is a test</p>',
            'tags': 'tag1,tag2,tag3',
            'to': 'groups-1'
        }
        resp = c.post('/mail/compose/', post_data)
        self.assertRedirects(resp, '/mail/schedule/')

        resp = c.get('/mail/schedule/')
        self.assertEquals(len(resp.context['schedule']), 1)

        email_id = resp.context['schedule'][0]['id']
        post_data['tags'] = 'tag2'
        resp = c.post('/mail/edit/{0}/'.format(email_id), post_data)
        self.assertRedirects(resp, '/mail/schedule/')


    def test_delete(self):
        c = Client()
        self.assertTrue(c.login(username='admin', password='password'))

        post_data = {
            'subject': 'Test subject',
            'body_text': '<p>This is a test</p>',
            'tags': 'tag1,tag2,tag3',
            'to': 'groups-1'
        }
        resp = c.post('/mail/compose/', post_data)
        self.assertRedirects(resp, '/mail/schedule/')

        resp = c.get('/mail/schedule/')
        self.assertEquals(len(resp.context['schedule']), 1)

        email_id = resp.context['schedule'][0]['id']
        resp = c.get('/mail/delete/{0}/'.format(email_id))
        self.assertRedirects(resp, '/mail/schedule/')


    @patch('mail.views.send_email')
    def test_send(self, *args):
        c = Client()
        self.assertTrue(c.login(username='admin', password='password'))

        post_data = {
            'subject': 'Test subject',
            'body_text': '<p>This is a test</p>',
            'tags': 'tag1,tag2,tag3',
            'to': 'groups-1'
        }
        resp = c.post('/mail/compose/', post_data)
        self.assertRedirects(resp, '/mail/schedule/')

        resp = c.get('/mail/send/1/')
        self.assertRedirects(resp, '/mail/schedule/')


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

