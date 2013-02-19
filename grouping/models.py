from groups import models as group_model
from signup import models as signup_model

import random

def group_users(max_group_size=20):

    # get all signups
    signups = signup_model.get_signups()
    groups = []

    # add to timezone buckets
    timezone_buckets = {}
    for signup in signups:
        #NOTE: this is an implicit requirement on the data needed in questions - not good!
        timezone = signup['questions']['timezone']
        if timezone in timezone_buckets:
            timezone_buckets[timezone] += [signup]
        else
            timezone_buckets[timezone] = [signup]

    # randomly group within timezone
    for timezone, signups in timezone_buckets.items():

        # create groups of max_group_size while there are enough signups
        timezone_groups = []
        while len(signups) > max_group_size:
            sample = random.sample(range(len(signups)), max_groups_size)
            timezone_groups.append({
                'timezone': timezone,
                'members': [signups[i] for i in sample]
            })
            signups = [s for s in signups if s not in sample]

        # distribute the remaining users between the timezone groups
        while len(timezone_groups) > 0 and len(signups) > 0:
            sample_groups = random.sample(timezone_groups, min(len(signups), len(timezone_groups)))
            for i, group in enumerate(sample_groups):
                group['members'].append(signups[i])

            del signups[:len(sample_groups)]

        groups += timezone_groups

    # group remaining signups with different timezones

    return groups

