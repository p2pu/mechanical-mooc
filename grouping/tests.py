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

