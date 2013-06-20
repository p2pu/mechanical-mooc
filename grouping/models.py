from django.conf import settings

from groups import models as group_model
from signup import models as signup_model
from mailgun import api as mailgun_api

import random
import math
import datetime
import pytz


def shuffle(rac):
    # shuffle items in a random access container
    shuffled = []
    while len(rac):
        ridx = random.randint(0, len(rac)-1)
        shuffled += [rac[ridx]]
        del rac[ridx]
    return shuffled


def prepare_groups(sequence, max_group_size=40):
    """ Do grouping for sequence """
     
    signups = signup_model.get_signups(sequence)
    tz_grouping = {}

    filter_group_preference = lambda su: su['questions']['groupRadios']
    for user_signup in filter(filter_group_preference, signups):
        timezone = user_signup['questions']['timezone']
        tz_offset = int(datetime.datetime.now(pytz.timezone(timezone)).strftime('%z'))
        user_signup['tz_offset'] = tz_offset
        if tz_offset in tz_grouping:
            tz_grouping[tz_offset].append(user_signup)
        else:
            tz_grouping[tz_offset] = [user_signup]

    for timezone, group in tz_grouping.items():
        tz_grouping[timezone] = shuffle(group)

    merge = lambda x,y: x + y
    tz_sorted_signups = reduce(merge, [ tz_grouping[timezone] for timezone in sorted(tz_grouping.keys())])

    groups = [ tz_sorted_signups[i:min(i+max_group_size, len(tz_sorted_signups))] for i in range(0,len(tz_sorted_signups), max_group_size)]

    return groups


def create_groups(groups, sequence, name_prefix="Group"):
    """ Create the groups in the backend """
    for i, group_data in enumerate(groups):
        group_address = "{0}-{1}@{2}".format(name_prefix.lower().replace(' ','-'), i+1, settings.EMAIL_DOMAIN)
        group_name = "{0} {1}: {2} to {3}".format(name_prefix, i+1, group_data[0]['tz_offset'], group_data[-1]['tz_offset'])
        print(group_name)

        group = group_model.create_group(group_address, group_name, sequence)

        for member in group_data:
            group_model.add_group_member(group['uri'], member['email'])


def do_grouping(sequence):
    groups = prepare_groups(sequence)
    create_groups(groups, sequence, 'Group {0}'.format(sequence))

    # handle singups not in group
    signups = signup_model.get_signups(sequence)
    filter_group_preference = lambda su: su['questions']['groupRadios'] == False
    signups = filter(filter_group_preference, signups)
    group_address = 'ungrouped-s-{0}@{1}'.format(sequence, settings.EMAIL_DOMAIN)
    group_name = 'Ungrouped S{0}'.format(sequence, settings.EMAIL_DOMAIN)
    ungroup = group_model.create_group(group_address, group_name, sequence)

    for signup in signups:
        group_model.add_group_member(ungroup['uri'], signup['email'])

    # sync groups with mailgun
    for group in group_model.get_groups(sequence):
        group_model.sync_group_with_mailgun(group['uri'])

    # update access to group for ungrouped users
    mailgun_api.update_list(ungroup, access_level='readonly')
