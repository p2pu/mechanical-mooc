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

        sequence = sequence_model.create_sequence(
            start_date, signup_close_date
        )

        self.assertEquals(sequence['start_date'], start_date)
        self.assertEquals(sequence['signup_close_date'], signup_close_date)
        self.assertTrue(self.create_list_patch.called)


    def test_get_current_sequence(self):
        current_sequence = sequence_model.get_current_sequence()

        self.assertEquals(current_sequence, None)

        now = datetime.datetime.utcnow().date()
        start_date = now + datetime.timedelta(weeks=8)
        signup_close_date = now + datetime.timedelta(weeks=7)

        sequence = sequence_model.create_sequence(
            start_date, signup_close_date
        )
        current_sequence = sequence_model.get_current_sequence()

        self.assertEqual(sequence, current_sequence)


    def test_multiple_sequences(self):
        now = datetime.datetime.utcnow().date()

        start_date = now - datetime.timedelta(weeks=16)
        signup_close_date = now - datetime.timedelta(weeks=17)
        sequence_model.create_sequence(
            start_date, signup_close_date
        )

        start_date = now + datetime.timedelta(weeks=8)
        signup_close_date = now + datetime.timedelta(weeks=7)
        sequence = sequence_model.create_sequence(
            start_date, signup_close_date
        )

        start_date = now + datetime.timedelta(weeks=16)
        signup_close_date = now + datetime.timedelta(weeks=15)
        sequence_model.create_sequence(
            start_date, signup_close_date
        )

        current_sequence = sequence_model.get_current_sequence()
        self.assertEqual(sequence, current_sequence)


    def test_get_all_sequences(self):
        now = datetime.datetime.utcnow().date()

        start_date = now - datetime.timedelta(weeks=16)
        signup_close_date = now - datetime.timedelta(weeks=17)
        sequence_model.create_sequence(
            start_date, signup_close_date
        )

        start_date = now + datetime.timedelta(weeks=8)
        signup_close_date = now + datetime.timedelta(weeks=7)
        sequence = sequence_model.create_sequence(
            start_date, signup_close_date
        )

        start_date = now + datetime.timedelta(weeks=16)
        signup_close_date = now + datetime.timedelta(weeks=15)
        sequence_model.create_sequence(
            start_date, signup_close_date
        )

        all_sequences = sequence_model.get_all_sequences()
        self.assertEqual(len(all_sequences), 3)
        self.assertEqual(sequence, all_sequences[1])
