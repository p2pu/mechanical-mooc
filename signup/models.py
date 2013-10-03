import random
import string
from datetime import datetime

from django.utils import simplejson

from signup import db
from signup import emails
from mailgun import api as mailgun_api
from sequence import models as sequence_model


def create_signup( email, questions ):
    if db.UserSignup.objects.filter(email=email, date_deleted__isnull=True).exists():
        raise Exception('Signup already exists')
    invite_code=''.join([
        random.choice(string.letters+string.digits) for i in range(32)
    ])
    sequence_number = sequence_model.get_current_sequence_number()
    now = datetime.utcnow()
    signup = db.UserSignup(
        email=email,
        invite_code=invite_code,
        questions=simplejson.dumps(questions),
        sequence=sequence_number,
        date_added=now,
        date_updated=now
    )
    signup.save()

    return get_signup(email)


def update_signup( email, questions ):
    """ will also add a signup to the latest sequence """
    signup_db = db.UserSignup.objects.get(email=email, date_deleted__isnull=True)
    
    old_questions = simplejson.loads(signup_db.questions)
    for key, value in questions.items():
        old_questions[key] = value

    signup_db.questions = simplejson.dumps(old_questions)
    signup_db.date_updated = datetime.utcnow()
    sequence = sequence_model.get_current_sequence_number()
    signup_db.sequence = sequence
    signup_db.save()


def create_or_update_signup( email, questions ):
    # check if user is already added
    if db.UserSignup.objects.filter(email=email, date_deleted__isnull=True).exists():
        return update_signup(email, questions)
    else:
        return create_signup(email, questions)


def delete_signup( email ):
    signup_db = db.UserSignup.objects.get(email=email, date_deleted__isnull=True)
    signup_db.date_deleted = datetime.utcnow()
    signup_db.save()
    

def _signup2json( signup_db ):
    signup = {
        'email': signup_db.email,
        'questions': simplejson.loads(signup_db.questions),
        'sequence': signup_db.sequence,
        'date_created': signup_db.date_added,
        'date_updated': signup_db.date_updated,
        'key': signup_db.invite_code
    }
    return signup


def get_signup( email ):
    if not db.UserSignup.objects.filter(email=email, date_deleted__isnull=True).exists():
        raise Exception()

    signup_db = db.UserSignup.objects.get(email=email, date_deleted__isnull=True)
    
    return _signup2json(signup_db)


def get_signup_by_invite_code( invite_code ):
    user_set = db.UserSignup.objects.filter(
        invite_code=invite_code,
        date_deleted__isnull=True
    )
    if not user_set.exists():
        raise Exception()

    return _signup2json(user_set[0])


def get_signups( sequence=None ):
    signups = db.UserSignup.objects.filter(date_deleted__isnull=True)
    if sequence:
        signups = signups.filter(sequence=sequence)
    return [_signup2json(signup) for signup in signups]


def get_new_signups( ):
    """ get signups where the welcome email hasn't been sent yet """
    signups = db.UserSignup.objects.filter(date_tasks_handled__isnull=True, date_deleted__isnull=True)
    return [_signup2json(signup) for signup in signups]


def remove_signup_from_sequence( email ):
    """ remove the signup from the sequence it is in and add it to the nexxt
        sequence if there is one.
    """
    signup_db = db.UserSignup.objects.get(email=email, date_deleted__isnull=True)
    
    sequence_number = sequence_model.get_current_sequence_number()
    if signup_db.sequence != sequence_number:
        signup_db.sequence = sequence_number
        signup_db.date_updated = datetime.utcnow()
        signup_db.date_tasks_handled = None
        signup_db.save()
    else:
        signup_db.sequence = None
        signup_db.date_updated = datetime.utcnow()
        signup_db.save()


def handle_new_signups( ):
    """ Send welcome email to new users.
        Add them to a general mailing list. 
        Update db when done. """
    signups = db.UserSignup.objects.filter(date_tasks_handled__isnull=True, date_deleted__isnull=True)[:500]
    while len(signups):
        emails.send_welcome_emails([signup.email for signup in signups])
        for signup in signups:
            add_user_to_global_list(signup.email)
            #make sure new signups aren't in the mailgun blocked list
            mailgun_api.delete_all_unsubscribes(signup.email)

        db.UserSignup.objects.filter(id__in=signups.values('id')).update(date_tasks_handled=datetime.utcnow())
        signups = db.UserSignup.objects.filter(date_tasks_handled__isnull=True, date_deleted__isnull=True)[:500]


def add_user_to_global_list( email ):
    """ add user to email list that gets all emails """
    signup_db = db.UserSignup.objects.get(email=email, date_deleted__isnull=True)
    if signup_db.sequence:
        list_name = sequence_model.sequence_list_name(signup_db.sequence)
        mailgun_api.add_list_member(list_name, email)
