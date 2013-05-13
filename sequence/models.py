from django.conf import settings

import db
from mailgun import api as mailgun_api

import datetime

def sequence2dict( sequence_db ):
    return {
        "id": sequence_db.id,
        "start_date": sequence_db.start_date,
        "signup_close_date": sequence_db.signup_close_date,
    }


def create_new_sequence( start_date, signup_close_date ):
    sequence_db = db.Sequence(
        start_date = start_date,
        signup_close_date = signup_close_date
    )
    sequence_db.save()

    mailgun_api.create_list(
        u'sequence-{0}-all@{1}'.format(sequence_db.id, settings.EMAIL_DOMAIN),
        'Sequence {0} global list'.format(sequence_db.id),
        'List for all members of sequence {0}'.format(sequence_db.id),
        'readonly'
    )

    return sequence2dict(sequence_db)


def get_current_sequence( ):
    sequence_db = db.Sequence.objects.filter(signup_close_date__gt=datetime.datetime.utcnow()).order_by('start_date')

    return sequence2dict(sequence_db[0])
