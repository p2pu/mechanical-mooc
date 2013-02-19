from groups import db


def group_uri2id( group_uri ):
    return group_uri.strip('/').split('/')[-1]


def group_id2uri( group_id ):
    return '/uri/group/{0}/'.format(group_id)


def create_group( address, description ):
    group_db = db.Group(address=address, description=description)
    group_db.save()
    #TODO create mailgun groups
    return get_group(group_id2uri(group_db.id))


def _group2json(group_db):
    group = {
        'uri': group_id2uri(group_db.id),
        'address': group_db.address,
        'description': group_db.description
    }
    group['members'] = [member.email for member in group_db.members.all()]
    return group
 


def get_group( group_uri ):
    group_id = group_uri2id(group_uri)
    group_db = db.Group.objects.get(id=group_id)
    return _group2json(group_db)


def get_groups():
    return [_group2json(group_db) for group_db in db.Group.objects.all()]


def add_group_member( group_uri, member_email ):
    group_id = group_uri2id(group_uri)
    group_db = db.Group.objects.get(id=group_id)
    member = db.GroupMember(email=member_email, group=group_db)
    member.save()


def remove_group_member( group_uri, member_email ):
    group_id = group_uri2id(group_uri)
    group_db = db.Group.objects.get(id=group_id)
    group_db.members.get(email=member_email).delete()
    
