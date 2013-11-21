from django.test import TestCase

from groups import models as group_model
from signup import models as signup_model
from signup import randata

from mock import patch
import random
import math

import models


@patch('signup.models.sequence_model.get_current_sequence_number', lambda: 1)
class SimpleTest(TestCase):
    def test_prepare_groups(self):
        for signup in randata.random_data(1000):
            signup_model.create_or_update_signup(**signup)

        groups = models.prepare_groups(1)

        grouped_users = filter(lambda x: x['questions']['groupRadios'], signup_model.get_signups(1))

        self.assertEquals(len(groups), math.ceil(len(grouped_users)/40.0))


    def test_every_man_is_an_island(self):
        for signup in randata.random_data(1000):
            signup_model.create_or_update_signup(**signup)

        groups = models.prepare_groups(1, max_group_size=1)

        for group in groups:
            self.assertEqual(len(group), 1)


    def test_here_comes_everyone(self):
        for signup in randata.random_data(1000):
            signup_model.create_or_update_signup(**signup)
        groups = models.prepare_groups(1, max_group_size=1001)
        self.assertEqual(len(groups), 1)


    def test_group_creation(self):
        for signup in randata.random_data(1000):
            signup_model.create_or_update_signup(**signup)

        
        group_data = models.prepare_groups(1)
        models.create_groups(group_data, 1)
        groups = group_model.get_groups(1)

        self.assertEqual(len(group_data), len(groups))
