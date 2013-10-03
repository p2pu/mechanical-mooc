from django.conf import settings
from django.template.loader import render_to_string

import mailgun

def send_confirmation_email( email, name, avatar, bio, confirmation_code ):
    context = {
        'email': email,
        'name': name,
        'avatar': avatar,
        'bio': bio,
        'confirmation_code': confirmation_code,
        'mooc_title': settings.MOOC_TITLE,
        'mooc_domain': settings.MOOC_DOMAIN
    }
    subject = render_to_string('gallery/emails/confirm-profile-subject.txt', context).strip()
    text_body = render_to_string('gallery/emails/confirm-profile.txt', context).strip()
    html_body = render_to_string('gallery/emails/confirm-profile.html', context).strip()
    mailgun.api.send_email(email, settings.DEFAULT_FROM_EMAIL, subject, text_body, html_body, tags=['bio_update'])


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
