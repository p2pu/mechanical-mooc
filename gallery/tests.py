from django.test import TestCase

from mock import patch

from gallery import models as gallery_api

@patch('signup.models.sequence_model.get_current_sequence_number', lambda: 1)
class SimpleTest(TestCase):

    def setUp(self):
        self.BIO_DATA = {
            'email': 'test@email.com',
            'name': 'Test User',
            'bio': 'This is some test data about a user',
            'avatar': 'http://some.url/image.png'
        }


    def test_save_bio(self):
        user_bio = gallery_api.save_bio(**self.BIO_DATA)
        self.assertEqual(self.BIO_DATA, user_bio)
        user_bio = gallery_api.get_bio(self.BIO_DATA['email'])
        self.assertEqual(self.BIO_DATA, user_bio)

    def test_get_sequence_bios(self):
        for i in range(10):
            data = self.BIO_DATA.copy()
            data['email'] = 'test-{0}@mail.com'.format(i)
            user_bio = gallery_api.save_bio(**data)

        bios = gallery_api.get_bios(1)
        self.assertEquals(len(bios), 10)

