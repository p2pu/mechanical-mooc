from django.core.management.base import BaseCommand, CommandError

from signup.models import send_welcome_emails

class Command(BaseCommand):
    help = 'Send welcome email to new signups'

    def handle(self, *args, **options):
        send_welcome_emails()
