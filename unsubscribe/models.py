from mailgun import api as mailgun_api
from signup import models as signup_model
from sequence import models as sequence_model
from groups import models as groups_model

import logging
log = logging.getLogger(__name__)


def unsubscribe_user( address ):
    """ Unsubscribe user completely from the Mechanical Mooc - all sequences
    """

    # remove from sequence group
    signups = signup_model.get_all_user_signups(address)
    for user_signup in signups:
        sequence_list = sequence_model.sequence_list_name(user_signup['sequence'])
        mailgun_api.remove_list_member(sequence_list, address)

    # remove from small groups
    groups = groups_model.get_member_groups(address)
    for group in groups:
        groups_model.remove_group_member(group['uri'], address)
        groups_model.sync_group_with_mailgun(group['uri'])

    # mark as unsubscribed in the signups
    for user_signup in signups:
        signup_model.delete_signup(address, user_signup['sequence'])

    mailgun_api.delete_all_unsubscribes(address)
