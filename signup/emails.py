from django.conf import settings
from django.template.loader import render_to_string

import mailgun

def send_welcome_emails(emails):
    subject = render_to_string('signup/emails/signup-confirmation-subject.txt', {}).strip()
    text_body = render_to_string('signup/emails/signup-confirmation.txt', {}).strip()
    html_body = render_to_string('signup/emails/signup-confirmation.html', {}).strip()
    mailgun.api.send_mass_email(emails, settings.DEFAULT_FROM_EMAIL, subject, text_body, html_body, tags=['signup'])
