from django.test import TestCase

from mock import patch

from gallery import models as gallery_api
from gallery import db

@patch('signup.models.sequence_model.get_current_sequence_number', lambda: 1)
class SimpleTest(TestCase):

    def setUp(self):
        self.BIO_DATA = {
            'email': 'test@email.com',
            'sequence': 1,
            'name': 'Test User',
            'bio': 'This is some test data about a user',
            'avatar': 'http://some.url/image.png'
        }


    def test_save_bio(self):
        user_bio = gallery_api.save_bio(**self.BIO_DATA)
        self.assertEqual(self.BIO_DATA, user_bio)


    def test_save_bio_with_twitter(self):
        bio_data = self.BIO_DATA.copy()
        bio_data['twitter'] = 'testhandle'
        user_bio = gallery_api.save_bio(**bio_data)
        self.assertEqual(bio_data, user_bio)


    def test_get_sequence_bios(self):
        for i in range(10):
            data = self.BIO_DATA.copy()
            data['email'] = 'test-{0}@mail.com'.format(i)
            user_bio = gallery_api.save_bio(**data)

        bios = gallery_api.get_bios(1)
        self.assertEquals(len(bios), 10)


    def test_update_bio(self):
        # create bio
        user_bio = gallery_api.save_bio(**self.BIO_DATA)

        # bio should now be in primary list of bios
        bios = gallery_api.get_bios(1)
        f = lambda x: x['email'] == user_bio['email']
        bios = filter(f, bios)
        self.assertEquals(len(bios), 1)
        self.assertEquals(bios[0], user_bio)

        # update bio
        update_data = self.BIO_DATA.copy()
        update_data['bio'] = 'This is the updated BIO'
        updated_bio = gallery_api.save_bio(**update_data)
       
        # new bio should now be displayed
        bios = gallery_api.get_bios(1)
        f = lambda x: x['email'] == user_bio['email']
        bios = filter(f, bios)
        self.assertEquals(len(bios), 1)
        self.assertEquals(bios[0], updated_bio)
