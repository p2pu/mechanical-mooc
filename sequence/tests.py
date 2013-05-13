"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from sequence import models as sequence_model
from mock import patch
import datetime

class SimpleTest(TestCase):

    def setUp(self):
        self.create_list_patcher = patch('sequence.models.mailgun_api.create_list')
        self.create_list_patch = self.create_list_patcher.start()


    def tearDown(self):
        self.create_list_patcher.stop()


    def test_create_sequence(self):
        now = datetime.datetime.utcnow().date()
        start_date = now + datetime.timedelta(weeks=8)
        signup_close_date = now + datetime.timedelta(weeks=7)

        sequence = sequence_model.create_new_sequence(
            start_date, signup_close_date
        )

        self.assertEquals(sequence['start_date'], start_date)
        self.assertEquals(sequence['signup_close_date'], signup_close_date)
        self.assertTrue(self.create_list_patch.called)

        start_date = now + datetime.timedelta(weeks=16)
        signup_close_date = now + datetime.timedelta(weeks=15)

        sequence_model.create_new_sequence(
            start_date, signup_close_date
        )

        current_sequence = sequence_model.get_current_sequence()
        self.assertEqual(sequence, current_sequence)
