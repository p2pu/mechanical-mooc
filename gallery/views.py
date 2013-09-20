from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django import http
from django.core.urlresolvers import reverse
from gallery import models as gallery_api
from gallery.utils import create_s3_policy_doc
from gallery.emails import send_confirmation_email

import hmac, hashlib
import random


def gallery(request):
    """ show gallery for all signups for this sequence with profiles """
    redirect_url = 'http://{0}/gallery/success/'.format(request.META.get('HTTP_HOST'))
    
    s3_policy, signature = create_s3_policy_doc(settings.AWS_S3_BUCKET, 'gallery', redirect_url)

    prefix = hmac.new('THEANSWERIS42', request.session.session_key, hashlib.sha1).hexdigest()

    bios = gallery_api.get_bios('TODO', limit=32)
    bios += [{'avatar': 'http://placehold.it/120x120', 'email': ''} for i in range(len(bios), 32)]
    bios = random.sample(bios, len(bios))

    # if user is logged in and has a bio, display it!
    user_bio = request.session.get('user_bio', None)
    if user_bio:
        bio_in_list = [ x for x in bios if x['email'] == user_bio['email'] ]
        if len(bio_in_list) == 1:
            # swap user bio with bio at position 12
            bio_index = bios.index(bio_in_list[0])
            bios[bio_index] = bios[11]
        bios[11] = user_bio
    else:
        # make a gap at position 12
        bios[11] = {'avatar': 'http://placehold.it/120x120'}


    context = {
        'bios': bios,
        'user_bio': user_bio,
        's3_policy': s3_policy,
        's3_signature': signature,
        's3_redirect_url': redirect_url,
        'AWS_ACCESS_KEY_ID': settings.AWS_ACCESS_KEY_ID,
        'AWS_S3_BUCKET': settings.AWS_S3_BUCKET,
        'key_prefix': 'gallery/{0}'.format(prefix)
    }
    
    return render_to_response('gallery/index.html', context, context_instance=RequestContext(request))


def save_bio(request):
    """ receive AJAX post from class gallery page """
    
    if request.method == 'POST':
        # save bio info
        user_bio = gallery_api.save_bio(
            request.POST['email'],
            request.POST['name'],
            request.POST['bio'],
            request.POST['avatar']
        )
        
        user_email = request.session.get('user_email', False)
        if user_email and user_email == user_bio['email']:
            user_bio = gallery_api.confirm_bio(user_bio['confirmation_code'])
        else:
            send_confirmation_email(**user_bio)
        
        request.session['user_bio'] = user_bio
    
    return http.HttpResponseRedirect(reverse('gallery_gallery'))


def avatar_success(request):
    return http.HttpResponse('')


def confirm_updates(request, confirmation_code):
    try:
        bio = gallery_api.confirm_bio(confirmation_code)
        request.session['user_bio'] = bio
        request.session['user_email'] = bio['email']
    except Exception:
        pass
    return http.HttpResponseRedirect(reverse('gallery_gallery'))
