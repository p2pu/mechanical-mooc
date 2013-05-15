import random
import string
from datetime import datetime

from django.utils import simplejson
from django.conf import settings

from signup import db
from signup import emails

from mailgun import api as mailgun_api

from sequence import models as sequence_model

def create_signup( email, questions ):
    if db.UserSignup.objects.filter(email=email).exists():
        raise Exception('Signup already exists')
    invite_code=''.join([
        random.choice(string.letters+string.digits) for i in range(32)
    ])
    current_sequence = sequence_model.get_current_sequence()
    now = datetime.utcnow()
    signup = db.UserSignup(
        email=email,
        invite_code=invite_code,
        questions=simplejson.dumps(questions),
        sequence=current_sequence['id'],
        date_added=now,
        date_updated=now
    )
    signup.save()

    return get_signup(email)


def update_signup( email, questions ):
    """ will also add a signup to the latest sequence """
    signup_db = db.UserSignup.objects.get(email=email)
    
    old_questions = simplejson.loads(signup_db.questions)
    for key, value in questions.items():
        old_questions[key] = value

    signup_db.questions = simplejson.dumps(old_questions)
    signup_db.date_updated = datetime.utcnow()
    current_sequence = sequence_model.get_current_sequence()
    signup_db.sequence = current_sequence['id']
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
        'sequence': signup_db.sequence,
        'date_created': signup_db.date_added,
        'date_updated': signup_db.date_updated
    }
    return signup


def get_signup( email ):
    if not db.UserSignup.objects.filter(email=email).exists():
        raise Exception()

    signup_db = db.UserSignup.objects.get(email=email)
    
    return _signup2json(signup_db)


def get_signups( sequence=None ):
    signups = db.UserSignup.objects.all()
    if sequence:
        signups = signups.filter(sequence=sequence)
    return [_signup2json(signup) for signup in signups]


def get_new_signups( ):
    """ get signups where the welcome email hasn't been sent yet """
    signups = db.UserSignup.objects.filter(date_welcome_email_sent__isnull=True)
    return [_signup2json(signup) for signup in signups]


def handle_new_signups( ):
    """ Send welcome email to new users.
        Add them to a general mailing list. 
        Update db when done. """
    signups = db.UserSignup.objects.filter(date_welcome_email_sent__isnull=True)[:500]
    while len(signups):
        emails.send_welcome_emails([signup.email for signup in signups])
        for signup in signups:
            add_user_to_global_list(signup.email)
        db.UserSignup.objects.filter(id__in=signups.values('id')).update(date_welcome_email_sent=datetime.utcnow())
        signups = db.UserSignup.objects.filter(date_welcome_email_sent__isnull=True)[:500]


def send_welcome_email( email ):
    """ send welcome email to user and update db """
    signup_db = db.UserSignup.objects.get(email=email)
    if signup_db.date_welcome_email_sent:
        raise Exception('Welcome email already sent!')
    emails.send_welcome_emails([signup_db.email])
    signup_db.date_welcome_email_sent = datetime.utcnow()
    signup_db.save()


def add_user_to_global_list( email ):
    """ add user to email list that gets all emails """
    current_sequence = sequence_model.get_current_sequence()
    if not current_sequence is None:
        mailgun_api.add_list_member('sequence-{0}-all@{1}'.format(current_sequence['id'], settings.EMAIL_DOMAIN), email)
