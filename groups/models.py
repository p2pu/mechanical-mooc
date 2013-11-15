from django.conf import settings

from groups import db
from mailgun import api as mailgun_api


def group_uri2id( group_uri ):
    return group_uri.strip('/').split('/')[-1]


def group_id2uri( group_id ):
    return '/uri/group/{0}/'.format(group_id)


def create_group( address, description, sequence ):
    group_db = db.Group(
        address=address, 
        description=description,
        sequence=sequence
    )
    group_db.save()
    return get_group(group_id2uri(group_db.id))


def _group2json(group_db):
    group = {
        'uri': group_id2uri(group_db.id),
        'address': group_db.address,
        'description': group_db.description,
        'sequence': group_db.sequence
    }
    group['members'] = [member.email for member in group_db.members.all()]
    return group


def get_group( group_uri ):
    group_id = group_uri2id(group_uri)
    group_db = db.Group.objects.get(id=group_id)
    return _group2json(group_db)


def get_groups( sequence=None ):
    groups = db.Group.objects.all()
    if sequence:
        groups = groups.filter(sequence=sequence)
    return [_group2json(group_db) for group_db in groups]


def get_member_groups( member_email ):
    membership = db.GroupMember.objects.filter(email__iexact=member_email)
    return [_group2json(member.group) for member in membership]


def add_group_member( group_uri, member_email ):
    group_id = group_uri2id(group_uri)
    group_db = db.Group.objects.get(id=group_id)
    if not group_db.members.filter(email__iexact=member_email).exists():
        member = db.GroupMember(email=member_email, group=group_db)
        member.save()


def remove_group_member( group_uri, member_email ):
    group_id = group_uri2id(group_uri)
    group_db = db.Group.objects.get(id=group_id)
    group_db.members.get(email__iexact=member_email).delete()


def sync_group_with_mailgun( group_uri ):
    group = get_group(group_uri)

    # check if group exists on mailgun, if not - create
    mg_group = mailgun_api.get_list(group['address'])
    if not mg_group:
        mailgun_api.create_list(group['address'], description=group['description'], access_level='members' )

    # get list of members
    mg_members = mailgun_api.get_list_members(group['address'])
    mg_member_set = [m['address'] for m in mg_members]

    # for every member locally not in mailgun, add them
    for member in group['members']:
        if member not in mg_member_set:
            # add member to mailgun
            mailgun_api.add_list_member(group['address'], member)

    # for every member on mailgun
    for member in mg_members:
        # if unsubscribed on mailgun, remove locally
        if member['subscribed'] == False and member['address'] in group['members']:
            # remove member from local group
            remove_group_member(group_uri, member['address'])

        # if on mailgun, but not locally, remove from mailgun
        if member['subscribed'] == True and member['address'] not in group['members']:
            mailgun_api.remove_list_member(group['address'], member['address'])

