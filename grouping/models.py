from groups import models as group_model
from signup import models as signup_model

import random
import math

def prepare_groups(max_group_size=20):
    """ Calculate grouping """

    # get all signups
    signups = signup_model.get_signups()

    for user_signup in signups:
        #NOTE: this is an implicit requirement on the data needed in questions - not good!
        timezone = user_signup['questions']['timezone']
        tz_offset = int(timezone[:timezone.index(' ')].replace(':',''))
        if tz_offset == -1200:
            tz_offset = 1200
        user_signup['tz_offset'] = tz_offset

    tz_sorted_signups = sorted(signups, key=lambda x: x['tz_offset'])
    groups = [ tz_sorted_signups[i:min(i+max_group_size, len(tz_sorted_signups))] for i in range(0,len(tz_sorted_signups), max_group_size)]
    return groups


def create_groups(groups, name_prefix="Group"):
    """ Create the groups in the backend """
    for i, group_data in enumerate(groups):
        group_address = "{0}-{1}@data.p2pu.org".format(name_prefix.lower().replace(' ','-'), i+1)
        group_name = "{0} {1}: {2} to {3}".format(name_prefix, i+1, group_data[0]['tz_offset'], group_data[-1]['tz_offset'])
        print(group_name)
        group = group_model.create_group(group_address, group_name)

        for member in group_data:
            group_model.add_group_member(group['uri'], member['email'])

