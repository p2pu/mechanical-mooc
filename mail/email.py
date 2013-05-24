from django.conf import settings
from django.template.loader import render_to_string

from mail import models as mail_api
from groups import models as group_api
from mailgun import api as mailgun_api
from sequence import models as sequence_api

def send_email( email_uri ):
    """ Send the email to the intended target audience """
    email = mail_api.get_email(email_uri)

    if email['audience'] == 'groups':
        to_address = ','.join([g['address'] for g in group_api.get_groups(email['sequence'])])
    elif email['audience'] == 'individuals':
        to_address = sequence_api.sequence_list_name(email['sequence'])

    text_body = render_to_string('mail/email.txt', {'email': email})
    html_body = render_to_string('mail/email.html', {'email': email})

    mailgun_api.send_email(
        to_address,
        settings.DEFAULT_FROM_EMAIL,
        email['subject'],
        text_body,
        html_body,
        email['tags'].split(','),
        sequence_api.sequence_campaign(email['sequence'])
    )
    mail_api.mark_sent(email_uri)
