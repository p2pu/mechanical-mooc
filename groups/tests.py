from django.test import TestCase

from groups import models as group_model

class SimpleTest(TestCase):
    def test_create_group(self):
        """
        Test group creation
        """
        group = group_model.create_group('ateam@mechmooc.com', 'The A team', '1')
        self.assertTrue('address' in group)
        self.assertTrue('description' in group)
        self.assertTrue('members' in group)
        self.assertTrue('sequence' in group)
        group_copy = group_model.get_group(group['uri'])
        self.assertEqual(group, group_copy)


    def test_add_group_member(self):
        group = group_model.create_group('ateam@mechmooc.com', 'The A team', '1')
        group_model.add_group_member(group['uri'], 'bob@mail.com')
        group = group_model.get_group(group['uri'])
        self.assertEqual(len(group['members']), 1)
        self.assertEqual(group['members'][0], 'bob@mail.com')


    def test_remove_group_member(self):
        group = group_model.create_group('ateam@mechmooc.com', 'The A team', '1')
        group_model.add_group_member(group['uri'], 'bob@mail.com')
        group_model.add_group_member(group['uri'], 'dick@mail.com')
        group_model.remove_group_member(group['uri'], 'dick@mail.com')
        group = group_model.get_group(group['uri'])
        self.assertEqual(len(group['members']), 1)
        self.assertEqual(group['members'][0], 'bob@mail.com')


    def test_get_sequence_groups(self):
        group = group_model.create_group('group-1-1@mechmooc.com', 'The A team', '1')
        group = group_model.create_group('group-1-2@mechmooc.com', 'The B team', '1')
        group = group_model.create_group('group-1-3@mechmooc.com', 'The C team', '1')
        group = group_model.create_group('group-1-4@mechmooc.com', 'The D team', '1')
        group = group_model.create_group('group-1-5@mechmooc.com', 'The E team', '1')

        group = group_model.create_group('group-2-1@mechmooc.com', 'The A team', '2')
        group = group_model.create_group('group-2-2@mechmooc.com', 'The B team', '2')
        group = group_model.create_group('group-2-3@mechmooc.com', 'The C team', '2')

        s_1_groups = group_model.get_groups('1')
        self.assertIn('group-1-1@mechmooc.com', [group['address'] for group in s_1_groups])
