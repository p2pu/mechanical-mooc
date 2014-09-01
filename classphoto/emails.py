from django.conf import settings
from django.template.loader import render_to_string
import json

import mailgun
from signup import models as signup_api
from sequence import models as sequence_api
from groups import models as group_api
from classphoto import group_photo

def send_user_link( email, key ):
    context = {
        'email': email,
        'key': key,
        'mooc_title': settings.MOOC_TITLE,
        'mooc_domain': settings.MOOC_DOMAIN
    }
    subject = render_to_string('classphoto/emails/user-link-subject.txt', context).strip()
    text_body = render_to_string('classphoto/emails/user-link.txt', context).strip()
    html_body = render_to_string('classphoto/emails/user-link.html', context).strip()
    mailgun.api.send_email(email, settings.DEFAULT_FROM_EMAIL, subject, text_body, html_body, tags=['user_link'])


def send_user_link_to_whole_sequence( sequence ):
    all_signups = signup_api.get_signups(sequence)
    context = {
        'mooc_title': settings.MOOC_TITLE,
        'mooc_domain': settings.MOOC_DOMAIN,
        'sequence': sequence
    }

    subject = render_to_string('classphoto/emails/sequence_links-subject.txt', context).strip()
    text_body = render_to_string('classphoto/emails/sequence_links.txt', context).strip()
    html_body = render_to_string('classphoto/emails/sequence_links.html', context).strip()

    for i in range(0, len(all_signups), 1000):
        signups = all_signups[i:i+1000]
        emails = [ signup['email'] for signup in signups ]
        recipient_variables = {
            signup['email']: {'key': signup['key']} for signup in signups
        }

        mailgun.api.send_mass_email(
            emails,
            settings.DEFAULT_FROM_EMAIL,
            subject,
            text_body,
            html_body,
            tags=['classphotolink'],
            campaign_id=sequence_api.sequence_campaign(sequence),
            recipient_variables=json.dumps(recipient_variables)
        )


def send_group_photos(sequence):

    context = {
        'mooc_title': settings.MOOC_TITLE,
        'mooc_domain': settings.MOOC_DOMAIN,
        'sequence': sequence,
    }

    urls = group_photo.make_group_photos(sequence)

    for group_uri, image_url in urls.items():
        group = group_api.get_group(group_uri)
        context['image_url'] = image_url
        subject = render_to_string(
            'classphoto/emails/sequence_group_photo-subject.txt', context
        ).strip()
        text_body = render_to_string(
            'classphoto/emails/sequence_group_photo.txt', context
        ).strip()
        html_body = render_to_string(
            'classphoto/emails/sequence_group_photo.html', context
        ).strip()

        mailgun.api.send_email(
            group['address'],
            settings.DEFAULT_FROM_EMAIL,
            subject,
            text_body,
            html_body,
            tags=['group_photo'],
            campaign_id=sequence_api.sequence_campaign(sequence)
        )
