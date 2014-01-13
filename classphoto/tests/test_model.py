from django.test import TestCase

from mock import patch

from classphoto import models as classphoto_api
from classphoto import db
from classphoto import emails

from signup import models as signup_api

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
        user_bio = classphoto_api.save_bio(**self.BIO_DATA)
        self.assertEqual(self.BIO_DATA, user_bio)


    def test_save_bio_with_twitter(self):
        bio_data = self.BIO_DATA.copy()
        bio_data['twitter'] = 'testhandle'
        user_bio = classphoto_api.save_bio(**bio_data)
        self.assertEqual(bio_data, user_bio)


    def test_save_bio_with_twitter(self):
        bio_data = self.BIO_DATA.copy()
        bio_data['gplus'] = 'http://plus.google.com/user/1231231231/'
        user_bio = classphoto_api.save_bio(**bio_data)
        self.assertEqual(bio_data, user_bio)


    def test_get_sequence_bios(self):
        for i in range(10):
            data = self.BIO_DATA.copy()
            data['email'] = 'test-{0}@mail.com'.format(i)
            user_bio = classphoto_api.save_bio(**data)

        bios = classphoto_api.get_bios(1)
        self.assertEquals(len(bios), 10)


    def test_get_sequence_bios_by_email(self):
        emails = ['test-{0}@mail.com'.format(i) for i in range(10)]
        for email in emails:
            data = self.BIO_DATA.copy()
            data['email'] = email
            user_bio = classphoto_api.save_bio(**data)
       
        bios = classphoto_api.get_bios_by_email(1, emails[:5])
        self.assertEquals(len(bios), 5)


    def test_update_bio(self):
        # create bio
        user_bio = classphoto_api.save_bio(**self.BIO_DATA)

        # bio should now be in primary list of bios
        bios = classphoto_api.get_bios(1)
        f = lambda x: x['email'] == user_bio['email']
        bios = filter(f, bios)
        self.assertEquals(len(bios), 1)
        self.assertEquals(bios[0], user_bio)

        # update bio
        update_data = self.BIO_DATA.copy()
        update_data['bio'] = 'This is the updated BIO'
        updated_bio = classphoto_api.save_bio(**update_data)
       
        # new bio should now be displayed
        bios = classphoto_api.get_bios(1)
        f = lambda x: x['email'] == user_bio['email']
        bios = filter(f, bios)
        self.assertEquals(len(bios), 1)
        self.assertEquals(bios[0], updated_bio)


    def test_send_user_link_to_whole_sequence( self ):
        signup_api.create_signup('mail1@mail.com', {})
        signup_api.create_signup('mail2@mail.com', {})
        signup_api.create_signup('mail3@mail.com', {})
        signup_api.create_signup('mail4@mail.com', {})
        signup_api.create_signup('mail5@mail.com', {})
        bio = self.BIO_DATA.copy()
        bio['email'] = 'mail1@mail.com'
        user_bio = classphoto_api.save_bio(**bio)
        bio['email'] = 'mail2@mail.com'
        user_bio = classphoto_api.save_bio(**bio)
        bio['email'] = 'mail3@mail.com'
        user_bio = classphoto_api.save_bio(**bio)
        bio['email'] = 'mail4@mail.com'
        user_bio = classphoto_api.save_bio(**bio)
        bio['email'] = 'mail5@mail.com'
        user_bio = classphoto_api.save_bio(**bio)

        with patch('classphoto.emails.mailgun.api.send_mass_email') as sme:
            emails.send_user_link_to_whole_sequence(1)
            self.assertTrue(sme.called)

