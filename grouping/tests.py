from django.test import TestCase

from groups import models as group_model
from signup import models as signup_model
from signup import randata

import models

import random

class SimpleTest(TestCase):
    def test_prepare_groups(self):
        for signup in randata.random_signup(1000):
            signup_model.create_or_update_signup(**signup)

        groups = models.prepare_groups()

        for i in range(100):
            random_group = random.choice(groups)
            random_user = random.choice(random_group['members'])

            self.assertEqual(random_group['timezone'], random_user['questions']['timezone'])


    def test_every_man_is_an_island(self):
        for signup in randata.random_signup(1000):
            signup_model.create_or_update_signup(**signup)

        groups = models.prepare_groups(max_group_size=1)

        for i in range(100):
            random_group = random.choice(groups)
            random_user = random.choice(random_group['members'])
            self.assertEqual(random_group['timezone'], random_user['questions']['timezone'])
            self.assertEqual(len(random_group['members']), 1)

    def test_here_comes_everyone(self):
        for signup in randata.random_signup(1000):
            signup_model.create_or_update_signup(**signup)
        groups = models.prepare_groups(max_group_size=1001)
        self.assertEqual(len(groups), 0)


    def test_group_creation(self):
        for signup in randata.random_signup(1000):
            signup_model.create_or_update_signup(**signup)

        group_data = models.prepare_groups()
        models.create_groups(group_data, 'g-')
        groups = group_model.get_groups()

        self.assertEqual(len(group_data), len(groups))
        for i, member in enumerate(groups[0]['members']):
            self.assertEqual(member, group_data[0]['members'][i]['email'])

