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
        del user_bio['confirmation_code']
        self.assertEqual(self.BIO_DATA, user_bio)
        user_bio = gallery_api.get_bio(self.BIO_DATA['email'])
        del user_bio['confirmation_code']
        self.assertEqual(self.BIO_DATA, user_bio)


    def test_save_bio_with_twitter(self):
        bio_data = self.BIO_DATA.copy()
        bio_data['twitter'] = 'testhandle'
        user_bio = gallery_api.save_bio(**bio_data)
        del user_bio['confirmation_code']
        self.assertEqual(bio_data, user_bio)


    def test_get_sequence_bios(self):
        for i in range(10):
            data = self.BIO_DATA.copy()
            data['email'] = 'test-{0}@mail.com'.format(i)
            user_bio = gallery_api.save_bio(**data)

        bios = gallery_api.get_bios(1)
        self.assertEquals(len(bios), 0)

        for bio in db.UserBio.objects.filter(date_deleted__isnull=True):
            gallery_api.confirm_bio(bio.confirmation_code)

        bios = gallery_api.get_bios(1)
        self.assertEquals(len(bios), 10)


    def test_update_bio(self):
        # create bio
        user_bio = gallery_api.save_bio(**self.BIO_DATA)

        # confirm bio
        bio = db.UserBio.objects.get(email=user_bio['email'])
        user_bio = gallery_api.confirm_bio(bio.confirmation_code)

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

        # old bio should still be displayed
        bios = gallery_api.get_bios(1)
        f = lambda x: x['email'] == user_bio['email']
        bios = filter(f, bios)
        self.assertEquals(len(bios), 1)
        self.assertEquals(bios[0], user_bio)

        # confirm bio
        bio = db.UserBio.objects.get(email=user_bio['email'], confirmation_code__isnull=False)
        updated_bio = gallery_api.confirm_bio(bio.confirmation_code)
       
        # new bio should now be displayed
        bios = gallery_api.get_bios(1)
        f = lambda x: x['email'] == user_bio['email']
        bios = filter(f, bios)
        self.assertEquals(len(bios), 1)
        self.assertEquals(bios[0], updated_bio)

