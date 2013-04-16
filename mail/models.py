import db
import datetime

def id2uri(id):
    return '/uri/mail/{0}'.format(id)


def uri2id(uri):
    return uri.strip('/').split('/')[-1]


def save_email(subject, text_body, html_body, tags):
    email_db = db.Email(
        subject=subject,
        text_body=text_body,
        html_body=html_body,
        tags = tags
    )
    email_db.save()
    return get_email(id2uri(email_db.id))


def update_email(uri, subject, text_body, html_body, tags):
    email_db = db.Email.objects.get(id=uri2id(uri))
    email_db.subject = subject
    email_db.text_body = text_body
    email_db.html_body = html_body
    email_db.tags = tags
    email_db.save()
    return get_email(uri)


def mark_sent(uri):
    email_db = db.Email.objects.get(id=uri2id(uri))
    email_db.date_sent = datetime.datetime.utcnow()
    email_db.save()


def delete_email(uri):
    email_db = db.Email.objects.get(id=uri2id(uri))
    email_db.delete()


def _2json(email_db):
    email_dict = {
        'id': email_db.id,
        'subject': email_db.subject,
        'text_body': email_db.text_body,
        'html_body': email_db.html_body,
        'tags': email_db.tags
    }
    if email_db.date_scheduled:
        email_dict['date_scheduled'] = email_db.date_scheduled
    if email_db.date_sent:
        email_dict['date_sent'] = email_db.date_sent
    return email_dict


def get_email(uri):
    email_db = db.Email.objects.get(id=uri2id(uri))
    return _2json(email_db)


def get_emails():
    return [_2json(em) for em in db.Email.objects.all()]


def schedule_email(uri, scheduled_datetime):
    email_db = db.Email.objects.get(id=uri2id(uri))
    email_db.date_scheduled = scheduled_datetime
    email_db.save()
