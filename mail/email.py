from django.conf import settings

from mail import models as mail_api
from groups import models as group_api
from mailgun import api as mailgun_api

def send_email_to_groups( email_uri ):
    email = mail_api.get_email(email_uri)
    group_addresses = ','.join([g['address'] for g in group_api.get_groups()])

    mailgun_api.send_email(
        group_addresses,
        settings.DEFAULT_FROM_EMAIL,
        email['subject'],
        email['text_body'],
        email['html_body'],
        email['tags'].split(',')
    )
    mail_api.mark_sent(email_uri)
