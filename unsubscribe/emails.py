from django.conf import settings
from django.template.loader import render_to_string

import mailgun


def send_unsubscribe_confirmation(signup):
    context = {
        'email': signup['email'],
        'key': signup['key'],
        'mooc_title': settings.MOOC_TITLE,
        'mooc_domain': settings.MOOC_DOMAIN
    }
    subject = render_to_string('unsubscribe/emails/confirm-subject.txt', context).strip()
    text_body = render_to_string('unsubscribe/emails/confirm.txt', context).strip()
    html_body = render_to_string('unsubscribe/emails/confirm.html', context).strip()

    mailgun.api.send_email(signup['email'], settings.DEFAULT_FROM_EMAIL,
        subject, text_body, html_body, tags=['user_link']
    )
