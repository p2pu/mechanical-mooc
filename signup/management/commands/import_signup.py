from django.core.management.base import BaseCommand, CommandError

from signup.models import create_or_update_signup

class Command(BaseCommand):
    args = '<data url>'
    help = 'Imports the specified signup data'

    def handle(self, *args, **options):
        import requests
        resp = requests.get(args[0])

        for signup in resp.json():
            email = signup['email']
            del signup['email']
            create_or_update_signup(email, signup)
