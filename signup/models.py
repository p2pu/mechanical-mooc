import random
import string
from datetime import datetime

from django.utils import simplejson

from signup import db
from signup.tasks import send_welcome_email

def create_signup( email, questions ):
    if db.UserSignup.objects.filter(email=email).exists():
        raise Exception('Signup already exists')
    invite_code=''.join([
        random.choice(string.letters+string.digits) for i in range(32)
    ])
    signup = db.UserSignup(
        email=email,
        invite_code=invite_code,
        questions=simplejson.dumps(questions),
        date_added=datetime.utcnow(),
        date_updated=datetime.utcnow()
    )
    signup.save()

    send_welcome_email.apply_async()

    return get_signup(email)


def update_signup( email, questions ):
    signup_db = db.UserSignup.objects.get(email=email)
    
    old_questions = simplejson.loads(signup_db.questions)
    for key, value in questions.items():
        old_questions[key] = value

    signup_db.questions = simplejson.dumps(old_questions)
    signup_db.date_updated=datetime.utcnow()
    signup_db.save()


def create_or_update_signup( email, questions ):
    # check if user is already added
    if db.UserSignup.objects.filter(email=email).exists():
        return update_signup(email, questions)
    else:
        return create_signup(email, questions)


def get_signup( email ):
    if not db.UserSignup.objects.filter(email=email).exists():
        raise Exception()

    signup_db = db.UserSignup.objects.get(email=email)
    
    signup = {
        'email': email,
        'questions': simplejson.loads(signup_db.questions),
        'date_created': signup_db.date_added,
        'date_updated': signup_db.date_updated
    }
    return signup


def create_group( ):
    return get_group('/uri/group/1')


def add_signup_to_group( email, group_uri ):
    pass


def remove_signup_from_group( email, group_uri ):
    pass


def get_group( group_uri ):
    group = {
        'uri': '/uri/groups/3',
        'members': [
            'dirk@p2pu.org',
            'bob@mail.com'
        ]
    }
