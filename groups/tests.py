from django.test import TestCase

from groups import models as group_model

class SimpleTest(TestCase):
    def test_create_group(self):
        """
        Test group creation
        """

        group = group_model.create_group('The A-Team')
        group_copy = group_model.get_group(group['uri'])

        for key, value in group.items():
            self.assertTrue(key in group_copy)
            self.assertEqual(value, group_copy[key])


    def test_add_group_member(self):
        group = group_model.create_group('The A team')
        group_model.add_group_member(group['uri'], 'bob@mail.com')
        group = group_model.get_group(group['uri'])
        self.assertEqual(len(group['members']), 1)
        self.assertEqual(group['members'][0], 'bob@mail.com')


    def test_remove_group_member(self):
        group = group_model.create_group('The A team')
        group_model.add_group_member(group['uri'], 'bob@mail.com')
        group_model.add_group_member(group['uri'], 'dick@mail.com')
        group_model.remove_group_member(group['uri'], 'dick@mail.com')
        group = group_model.get_group(group['uri'])
        self.assertEqual(len(group['members']), 1)
        self.assertEqual(group['members'][0], 'bob@mail.com')
