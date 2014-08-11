import random
import string
from datetime import datetime

import json

from signup import db
from signup import emails
from mailgun import api as mailgun_api
from sequence import models as sequence_model


def create_signup( email, questions ):
    """ Add signup to the current sequence """
    sequence = sequence_model.get_current_sequence_number()
    if db.UserSignup.objects.filter(email__iexact=email, sequence=sequence).exists():
        raise Exception('Signup already exists')
    invite_code=''.join([
        random.choice(string.letters+string.digits) for i in range(32)
    ])
    now = datetime.utcnow()
    signup = db.UserSignup(
        email=email,
        invite_code=invite_code,
        questions=json.dumps(questions),
        sequence=sequence,
        date_added=now,
        date_updated=now
    )
    signup.save()
    return _signup2json(signup)


def update_signup( email, questions ):
    """ Update the signup if it exists for the current sequence. If the signup was previously delete it will be undeleted """
    sequence = sequence_model.get_current_sequence_number()
    signup_db = db.UserSignup.objects.get(email__iexact=email, sequence=sequence)

    old_questions = json.loads(signup_db.questions)
    for key, value in questions.items():
        old_questions[key] = value

    signup_db.questions = json.dumps(old_questions)
    signup_db.date_updated = datetime.utcnow()
    signup_db.date_deleted = None
    signup_db.save()
    return _signup2json(signup_db)


def create_or_update_signup( email, questions ):
    # check if user is already added to the current sequence
    sequence = sequence_model.get_current_sequence_number()
    if db.UserSignup.objects.filter(email__iexact=email, sequence=sequence).exists():
        return update_signup(email, questions)
    else:
        return create_signup(email, questions)


def delete_signup( email, sequence ):
    if db.UserSignup.objects.filter(email__iexact=email, sequence=sequence, date_deleted__isnull=False).exists():
        raise Exception('Signup already deleted')
    signup_db = db.UserSignup.objects.get(email__iexact=email, sequence=sequence)
    signup_db.date_deleted = datetime.utcnow()
    signup_db.save()
    

def _signup2json( signup_db ):
    signup = {
        'email': signup_db.email,
        'questions': json.loads(signup_db.questions),
        'sequence': signup_db.sequence,
        'date_created': signup_db.date_added,
        'date_updated': signup_db.date_updated,
        'date_deleted': signup_db.date_deleted,
        'key': signup_db.invite_code
    }
    return signup


def get_signup( email, sequence ):
    if not db.UserSignup.objects.filter(email__iexact=email, sequence=sequence, date_deleted__isnull=True).exists():
        raise Exception(u'Signup for {0} not found'.format(email))

    signup_db = db.UserSignup.objects.get(email__iexact=email, sequence=sequence, date_deleted__isnull=True)
    
    return _signup2json(signup_db)


def get_all_user_signups( email ):
    signups = db.UserSignup.objects.filter(email__iexact=email, date_deleted__isnull=True)
    return [ _signup2json(su) for su in signups ]


def get_signup_by_invite_code( invite_code ):
    user_set = db.UserSignup.objects.filter(
        invite_code=invite_code,
        date_deleted__isnull=True
    )
    if not user_set.exists():
        raise Exception()

    return _signup2json(user_set[0])


def get_signups( sequence ):
    signups = db.UserSignup.objects.filter(date_deleted__isnull=True)
    if sequence:
        signups = signups.filter(sequence=sequence)
    return [_signup2json(signup) for signup in signups]


def get_signups_for_archiving( sequence ):
    """ Only use this for archiving."""
    sequence = int(sequence)
    # TODO this is messy!
    signups = db.UserSignup.objects.raw('select distinct on (email) * from signup_usersignup where sequence= '+ str(sequence) +' order by email, date_added DESC;')
    return [_signup2json(signup) for signup in signups]


def get_new_signups( ):
    """ get signups where the welcome email hasn't been sent yet """
    signups = db.UserSignup.objects.filter(date_tasks_handled__isnull=True, date_deleted__isnull=True)
    return [_signup2json(signup) for signup in signups]


def handle_new_signups( ):
    """ Send welcome email to new users.
        Add them to a general mailing list. 
        Update db when done. """
    signups = db.UserSignup.objects.filter(date_tasks_handled__isnull=True, date_deleted__isnull=True)[:500]
    while len(signups):
        #TODO emails.send_welcome_emails([signup.email for signup in signups])
        for signup in signups:
            add_user_to_global_list(signup.email, signup.sequence)
            #make sure new signups aren't in the mailgun blocked list
            mailgun_api.delete_all_unsubscribes(signup.email)

        db.UserSignup.objects.filter(id__in=signups.values('id')).update(date_tasks_handled=datetime.utcnow())
        signups = db.UserSignup.objects.filter(date_tasks_handled__isnull=True, date_deleted__isnull=True)[:500]


def add_user_to_global_list( email, sequence ):
    """ add user to email list that gets all emails """
    signup_db = db.UserSignup.objects.get(
        email__iexact=email, date_deleted__isnull=True, sequence=sequence
    )
    if signup_db.sequence:
        list_name = sequence_model.sequence_list_name(signup_db.sequence)
        mailgun_api.add_list_member(list_name, email)
