from django.core.management.base import BaseCommand, CommandError

from mail import models as mail_api
from mail.email import send_email

from datetime import datetime

class Command(BaseCommand):
    #args = '<data url>'
    help = 'Send all scheduled email with a date in the past'

    def handle(self, *args, **options):
        emails = mail_api.get_emails()
        for email in emails:
            date_scheduled = email.get('date_scheduled')
            date_sent = email.get('date_sent')
            if not date_sent and date_scheduled and date_scheduled < datetime.utcnow():
                print(u'sending email {0}'.format(email['subject']))
                send_email(email['uri'])
                #TODO maybe send an email to site admin?
