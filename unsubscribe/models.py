from mailgun import api as mailgun_api
from signup import models as signup_model
from sequence import models as sequence_model
from groups import models as groups_model

def unsubscribe_from_sequence( address ):

    user_signup = signup_model.get_signup(address)

    # remove from sequence group
    sequence_list = sequence_model.sequence_list_name(user_signup['sequence'])
    try:
        mailgun_api.remove_list_member(sequence_list, address)
    except:
        # TODO: log error
        pass
    
    # remove from small groups
    # TODO: Can a user be subscribed to more than one group or more than one
    # sequence at the same time?
    groups = groups_model.get_member_groups(address)
    for group in groups:
        groups_model.remove_group_member(group['uri'], address)
        groups_model.sync_group_with_mailgun(group['uri'])

    # add signup to next sequence.
    signup_model.remove_signup_from_sequence(address)


def unsubscribe_user( address ):
    """ Unsubscribe user completely from the Mechanical Mooc 
    """
    user_signup = signup_model.get_signup(address)

    # remove from sequence group
    sequence_list = sequence_model.sequence_list_name(user_signup['sequence'])
    try:
        mailgun_api.remove_list_member(sequence_list, address)
    except:
        # TODO: log error
        pass

    # remove from small groups
    groups = groups_model.get_member_groups(address)
    for group in groups:
        groups_model.remove_group_member(group['uri'], address)
        groups_model.sync_group_with_mailgun(group['uri'])

    # mark as unsubscribed in the signups
    signup_model.delete_signup(address)
    
    # remove from mailgun unsubscribes so that user can subscribe again
    mailgun_api.delete_all_unsubscribes(address)
