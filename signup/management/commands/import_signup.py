from django.core.management.base import BaseCommand, CommandError

from signup.models import create_or_update_signup
from signup.models import add_user_to_global_list
from signup import db

import datetime

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
            db.UserSignup.objects.filter(email=email).update(date_welcome_email_sent=datetime.datetime.utcnow())
            add_user_to_global_list(email)
