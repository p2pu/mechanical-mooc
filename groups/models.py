from groups import db


def group_uri2id( group_uri ):
    return group_uri.strip('/').split('/')[-1]


def group_id2uri( group_id ):
    return '/uri/group/{0}/'.format(group_id)


def create_group( group_name ):
    group_db = db.Group(name=group_name)
    group_db.save()
    return get_group(group_id2uri(group_db.id))


def get_group( group_uri ):
    group_id = group_uri2id(group_uri)
    group_db = db.Group.objects.get(id=group_id)
    group = {
        'uri': group_id2uri(group_db.id),
        'name': group_db.name,
    }
    group['members'] = [member.email for member in group_db.members.all()]
    return group


def add_group_member( group_uri, member_email ):
    group_id = group_uri2id(group_uri)
    group_db = db.Group.objects.get(id=group_id)
    member = db.GroupMember(email=member_email, group=group_db)
    member.save()


def remove_group_member( group_uri, member_email ):
    group_id = group_uri2id(group_uri)
    group_db = db.Group.objects.get(id=group_id)
    group_db.members.get(email=member_email).delete()
    
