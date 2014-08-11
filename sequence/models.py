from django.conf import settings

import db
from mailgun import api as mailgun_api

import datetime


def sequence_list_name( sequence_number ):
    if settings.DEBUG:
        return '{0}-{1}-all-test@{2}'.format(settings.MOOC_TITLE.replace(' ', '-').lower(), sequence_number, settings.EMAIL_DOMAIN)
    return '{0}-{1}-all@{2}'.format(settings.MOOC_TITLE.replace(' ', '-').lower(), sequence_number, settings.EMAIL_DOMAIN)


def sequence_campaign( sequence_number ):
    if settings.DEBUG:
        return '{0}-{1}-campaign-test'.format(settings.MOOC_TITLE.replace(' ', '-').lower(), sequence_number)
    return '{0}-{1}-campaign'.format(settings.MOOC_TITLE.replace(' ', '-').lower(), sequence_number)


def sequence2dict( sequence_db ):
    return {
        'id': sequence_db.id,
        'start_date': sequence_db.start_date,
        'signup_close_date': sequence_db.signup_close_date,
        'global_list': sequence_list_name(sequence_db.id),
        'campaign_id': sequence_campaign(sequence_db.id)
    }


def create_sequence( start_date, signup_close_date ):
    sequence_db = db.Sequence(
        start_date = start_date,
        signup_close_date = signup_close_date
    )
    sequence_db.save()

    mailgun_api.create_list(
        sequence_list_name(sequence_db.id),
        'Sequence {0} global list'.format(sequence_db.id),
        'List for all members of sequence {0}'.format(sequence_db.id),
        'readonly'
    )

    mailgun_api.create_campaign(
        sequence_campaign(sequence_db.id),
        'Sequence {0} campaign'.format(sequence_db.id)
    )

    return sequence2dict(sequence_db)


def get_all_sequences( ):
    return [ sequence2dict(seq) for seq in db.Sequence.objects.all() ]


def get_current_sequence( ):
    """ return the first sequence where signup_close_date is in the future """
    sequence_db = db.Sequence.objects.filter(signup_close_date__gte=datetime.datetime.utcnow().date()).order_by('start_date')

    if sequence_db.count() == 0:
        return None

    return sequence2dict(sequence_db[0])


def get_current_sequence_number( ):
    sequence_db = db.Sequence.objects.filter(signup_close_date__gte=datetime.datetime.utcnow().date()).order_by('start_date')

    if sequence_db.count() == 0:
        return None

    return sequence_db[0].id
