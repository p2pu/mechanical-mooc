from celery import task

@task
def send_welcome_email(email):
    pass
