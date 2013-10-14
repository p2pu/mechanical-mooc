from django.conf import settings
from django.template.loader import render_to_string
from django.utils import simplejson as json

import mailgun
from signup import models as signup_api


def send_user_link( email, key ):
    context = {
        'email': email,
        'key': key,
        'mooc_title': settings.MOOC_TITLE,
        'mooc_domain': settings.MOOC_DOMAIN
    }
    subject = render_to_string('gallery/emails/user-link-subject.txt', context).strip()
    text_body = render_to_string('gallery/emails/user-link.txt', context).strip()
    html_body = render_to_string('gallery/emails/user-link.html', context).strip()
    mailgun.api.send_email(email, settings.DEFAULT_FROM_EMAIL, subject, text_body, html_body, tags=['user_link'])


def send_user_link_to_whole_sequence( sequence ):
    signups = signup_api.get_signups(sequence)
    emails = [ signup['email'] for signup in signups ]
    recipient_variables = {
        signup['email']: {'key': signup['key']} for signup in signups
    }

    context = {
        'mooc_title': settings.MOOC_TITLE,
        'mooc_domain': settings.MOOC_DOMAIN,
        'sequence': sequence
    }

    subject = render_to_string('gallery/emails/sequence_links-subject.txt', context).strip()
    text_body = render_to_string('gallery/emails/sequence_links.txt', context).strip()
    html_body = render_to_string('gallery/emails/sequence_links.html', context).strip()

    #TODO: send in batches of 1000 emails
    #TODO: include campaign id for sequence 
    mailgun.api.send_mass_email(
        emails,
        settings.DEFAULT_FROM_EMAIL,
        subject,
        text_body,
        html_body,
        tags=['classphotolink'],
        recipient_variables=json.dumps(recipient_variables)
    )

