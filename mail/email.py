from django.conf import settings

from mail import models as mail_api
from groups import models as group_api
from mailgun import api as mailgun_api

def send_email( email_uri ):
    """ Send the email to the intended target audience """
    email = mail_api.get_email(email_uri)

    if email['audience'] == 'groups':
        to_address = ','.join([g['address'] for g in group_api.get_groups(email['sequence'])])
    elif email['audience'] == 'individuals':
        to_address = 'sequence-{0}-all@{1}'.format(email['sequence'], settings.EMAIL_DOMAIN)

    mailgun_api.send_email(
        to_address,
        settings.DEFAULT_FROM_EMAIL,
        email['subject'],
        email['text_body'],
        email['html_body'],
        email['tags'].split(','),
        'sequence-{0}-campaign'
    )
    mail_api.mark_sent(email_uri)
