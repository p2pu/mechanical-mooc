from gallery import db

import datetime
import string
import random

def _bio2dict( bio_db ):
    return { 
        'email': bio_db.email,
        'name': bio_db.name,
        'bio': bio_db.bio,
        'avatar': bio_db.avatar,
        'confirmation_code': bio_db.confirmation_code
    }


def save_bio( email, name, bio, avatar ):
    
    now = datetime.datetime.utcnow()

    # if we do and it is pending, just delete it
    # if we do and it is confirmed, just add new
    if db.UserBio.objects.filter(email=email, date_deleted__isnull=True, confirmation_code__isnull=False).exists():
        pending_bio = db.UserBio.objects.get(email=email, date_deleted__isnull=True, confirmation_code__isnull=False)
        pending_bio.date_deleted = now
        pending_bio.save()

    bio_db = db.UserBio()
    bio_db.email = email
    bio_db.name = name
    bio_db.bio = bio
    bio_db.avatar = avatar
    bio_db.date_added = now
    bio_db.date_updated = now
    bio_db.confirmation_code = ''.join([random.choice(string.letters + string.digits) for i in range(32)])
    bio_db.save()
    return _bio2dict(bio_db)


def confirm_bio( confirmation_code ):
    bio_db = db.UserBio.objects.get(confirmation_code=confirmation_code)

    if db.UserBio.objects.filter(email=bio_db.email, date_deleted__isnull=True, confirmation_code__isnull=True).exists():
        old_bio = db.UserBio.objects.get(email=bio_db.email, date_deleted__isnull=True, confirmation_code__isnull=True)
        old_bio.date_deleted = datetime.datetime.utcnow()
        old_bio.save()

    bio_db.confirmation_code = None
    bio_db.save()
    return _bio2dict(bio_db)


def get_bio( email ):
    return _bio2dict(db.UserBio.objects.get(email=email))


def get_bios( sequence ):
    bios_db = db.UserBio.objects.filter(confirmation_code__isnull=True, date_deleted__isnull=True)
    return [ _bio2dict(bio) for bio in bios_db ]
