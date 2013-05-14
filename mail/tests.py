"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from mail import models as mail_model

import datetime

class SimpleTest(TestCase):
    email_params = [
        'The subject',
        'The text body',
        '<html></html>',
        '1',
        'groups',
        'tag1,tag2,tag3'
    ]

    def test_save_email(self):
        email = mail_model.save_email(*self.email_params)
        email2 = mail_model.get_email(email['uri'])
        self.assertEqual(email, email2)


    def test_get_emails(self):
        email = mail_model.save_email(*self.email_params)
        mail_model.save_email(*self.email_params)
        mail_model.save_email(*self.email_params)
        mail_model.save_email(*self.email_params)

        all_mail = mail_model.get_emails()
        self.assertEqual(len(all_mail), 4)


    def test_update_email(self):
        email = mail_model.save_email(*self.email_params)
        mail_model.update_email(email['uri'], 'New sub', 'New Text', '', '2', 'individuals', 'tag1')
        email2 = mail_model.get_email(email['uri'])
        self.assertNotEqual(email, email2)
        self.assertEqual(email2['subject'], 'New sub')
        self.assertEqual(email2['text_body'], 'New Text')
        self.assertEqual(email2['html_body'], '')
        self.assertEqual(email2['sequence'], '2')
        self.assertEqual(email2['audience'], 'individuals')
        self.assertEqual(email2['tags'], 'tag1')


    def test_mark_sent(self):
        email = mail_model.save_email(*self.email_params)
        mail_model.mark_sent(email['uri'])
        email2 = mail_model.get_email(email['uri'])
        self.assertIn('date_sent', email2.keys())


    def test_delete_email(self):
        email = mail_model.save_email(*self.email_params)
        email = mail_model.save_email(*self.email_params)
        mail_model.delete_email(email['uri'])
        with self.assertRaises(Exception):
            email2 = mail_model.get_email(email['uri'])


    def test_schedule_email(self):
        email = mail_model.save_email(*self.email_params)
        mail_model.schedule_email(email['uri'], datetime.datetime.utcnow())
        email2 = mail_model.get_email(email['uri'])
        self.assertIn('date_scheduled', email2.keys())


    def test_get_sequence_emails(self):
        pass

