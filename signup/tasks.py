from celery import task

import emails

@task
def send_welcome_email(email):
    """ Celery task to send email asynchronously """
    emails.send_welcome_email(email)
