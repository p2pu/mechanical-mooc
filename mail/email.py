from django.conf import settings
from django.template.loader import render_to_string

from mail import models as mail_api
from groups import models as group_api
from mailgun import api as mailgun_api
from sequence import models as sequence_api
from classphoto.models import get_bios_by_email

def send_email( email_uri ):
    """ Send the email to the intended target audience """
    email = mail_api.get_email(email_uri)

    recipient_variables = {}
    if email['audience'] == 'groups':
        groups = group_api.get_groups(email['sequence'])
        to_address = ','.join([g['address'] for g in groups])
        for group in groups:
            recipient_variables['email'] = {}
            bios = get_bios_by_email(email['sequence'], group['members'])
            if len(bios) > 0:
                context = {'bios': bios}
                bios_snip = render_to_string('classphoto/emails/group_intro.html', context)
                recipient_variables['email']['bios_snip'] = bios_snip
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
        sequence_api.sequence_campaign(email['sequence']),
        recipient_variables
    )
    mail_api.mark_sent(email_uri)
