from gallery import db
import datetime

def _bio2dict( bio_db ):
    return { 
        'email': bio_db.email,
        'name': bio_db.name,
        'bio': bio_db.bio,
        'avatar': bio_db.avatar
    }


def save_bio( email, name, bio, avatar ):
    now = datetime.datetime.utcnow()
    bio_db, created = db.UserBio.objects.get_or_create(email=email, 
        defaults={'date_added': now, 'date_updated': now} )
    bio_db.name = name
    bio_db.bio = bio
    bio_db.avatar = avatar
    bio_db.date_updated = datetime.datetime.utcnow()
    bio_db.save()
    return _bio2dict(bio_db)


def get_bio( email ):
    return _bio2dict(db.UserBio.objects.get(email=email))


def get_bios( sequence ):
    bios_db = db.UserBio.objects.all()
    return [ _bio2dict(bio) for bio in bios_db ]
