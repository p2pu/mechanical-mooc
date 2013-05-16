from django.core.management.base import BaseCommand, CommandError

from signup.models import handle_new_signups

class Command(BaseCommand):
    help = 'Send welcome emails to new signups and add users to global mailing list.'

    def handle(self, *args, **options):
        handle_new_signups()
