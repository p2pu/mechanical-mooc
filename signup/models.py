import random
import string
from datetime import datetime

from django.utils import simplejson

from signup import db
from signup import emails

def create_signup( email, questions ):
    if db.UserSignup.objects.filter(email=email).exists():
        raise Exception('Signup already exists')
    invite_code=''.join([
        random.choice(string.letters+string.digits) for i in range(32)
    ])
    now = datetime.utcnow()
    signup = db.UserSignup(
        email=email,
        invite_code=invite_code,
        questions=simplejson.dumps(questions),
        date_added=now,
        date_updated=now
    )
    signup.save()

    return get_signup(email)


def update_signup( email, questions ):
    signup_db = db.UserSignup.objects.get(email=email)
    
    old_questions = simplejson.loads(signup_db.questions)
    for key, value in questions.items():
        old_questions[key] = value

    signup_db.questions = simplejson.dumps(old_questions)
    signup_db.date_updated = datetime.utcnow()
    signup_db.save()


def create_or_update_signup( email, questions ):
    # check if user is already added
    if db.UserSignup.objects.filter(email=email).exists():
        return update_signup(email, questions)
    else:
        return create_signup(email, questions)


def _signup2json( signup_db ):
    signup = {
        'email': signup_db.email,
        'questions': simplejson.loads(signup_db.questions),
        'date_created': signup_db.date_added,
        'date_updated': signup_db.date_updated
    }
    return signup


def get_signup( email ):
    if not db.UserSignup.objects.filter(email=email).exists():
        raise Exception()

    signup_db = db.UserSignup.objects.get(email=email)
    
    return _signup2json(signup_db)


def get_signups( ):
    return [_signup2json(signup) for signup in db.UserSignup.objects.all()]


def get_new_signups( ):
    """ get signups where the welcome email hasn't been sent yet """
    signups = db.UserSignup.objects.filter(date_welcome_email_sent__isnull=True)
    return [_signup2json(signup) for signup in signups]


def send_welcome_email( email ):
    """ send welcome email to user and update db """
    signup_db = db.UserSignup.objects.get(email=email)
    if signup_db.date_welcome_email_sent:
        raise Exception('Welcome email already sent!')
    emails.send_welcome_email(signup_db.email)
    signup_db.date_welcome_email_sent = datetime.utcnow()
    signup_db.save()

