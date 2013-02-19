from django.test import TestCase

from groups import models as group_model
from signup import models as signup_model
from signup import randata

import models

import random

class SimpleTest(TestCase):
    def test_grouping(self):
        for signup in randata.random_signup(1000):
            signup_model.create_or_update_signup(**signup)

        groups = models.create_groups()

        for i in range(100):
            random_group = random.choice(groups)
            random_user = random.choice(random_group['members'])

            self.assertEqual(random_group['timezone'], random_user['questions']['timezone'])


    def test_every_man_is_an_island(self):
        for signup in randata.random_signup(1000):
            signup_model.create_or_update_signup(**signup)

        groups = models.create_groups(max_group_size=1)

        for i in range(100):
            random_group = random.choice(groups)
            random_user = random.choice(random_group['members'])
            self.assertEqual(random_group['timezone'], random_user['questions']['timezone'])
            self.assertEqual(len(random_group['members']), 1)

    def test_here_comes_everyone(self):
        for signup in randata.random_signup(1000):
            signup_model.create_or_update_signup(**signup)
        groups = models.create_groups(max_group_size=1001)
        self.assertEqual(len(groups), 0)

