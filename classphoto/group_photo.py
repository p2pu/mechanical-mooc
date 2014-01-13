from models import get_bios_by_email
from groups import models as group_model

import requests
import math
from PIL import Image
import boto
from boto.s3.key import Key
from django.conf import settings


def combine_photos(bios, width=6, avatar_size=(120,120)):
    # download images and sticth them together
    images = []
    for bio in bios:
        try:
            resp = requests.get(bio['avatar'], stream=True)
            with open('/tmp/' + bio['email'], 'wb') as f:
                for chunk in resp.iter_content(chunk_size=1024): 
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
                        f.flush()
            images += [ '/tmp/' + bio['email'] ]
        except Exception as e:
            print(e)

    image_width = min(width, len(images))*avatar_size[0]
    image_height = int(math.ceil(1.0*len(images)/width)*avatar_size[1])
    collage = Image.new('RGB', (image_width, image_height))
    for index, image in enumerate(images):
        x = index%width
        y = index/width
        try:
            avatar = Image.open(image)
            avatar.thumbnail(avatar_size, Image.ANTIALIAS)
            collage.paste(avatar, (x*avatar_size[0], y*avatar_size[1]))
        except Exception as e:
            print(e)
    return collage


def make_group_photo(group_uri):
    group = group_model.get_group(group_uri)
    bios = get_bios_by_email(group['sequence'], group['members'])
    group_photo = combine_photos(bios)
    file_name = u'gf_{0}.jpg'.format(group_uri.strip('/').split('/')[-1])
    group_photo.save(file_name, u'JPEG')
    return file_name


def upload_to_s3(filename, bucket):
    c = boto.connect_s3()
    b = c.get_bucket(bucket)
    k = Key(b)
    k.key = filename
    k.set_contents_from_filename(filename, policy='public-read')
    return k.generate_url(expires_in=0, query_auth=False, force_http=True)


def make_group_photos(sequence):
    groups = group_model.get_groups(sequence)
    photos = {}
    for group in groups:
        photos[group['uri']] = make_group_photo(group['uri'])

    photo_urls = {}
    for group_uri in photos:
        photo_urls[group_uri] = upload_to_s3(photos[group_uri], settings.AWS_S3_BUCKET)

    return photo_urls
