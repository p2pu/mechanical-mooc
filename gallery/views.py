from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django import http
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from gallery import models as gallery_api
from gallery.utils import create_s3_policy_doc
from gallery.emails import send_confirmation_email

from signup import models as signup_api

import hmac, hashlib
import random


def gallery(request):
    """ show gallery for all signups for this sequence with profiles """
    s3_policy, signature = create_s3_policy_doc(settings.AWS_S3_BUCKET, 'gallery')

    messages.error(request, 'Test this')

    if request.GET.get('key'):
        pass

    prefix = hmac.new(
        'THEANSWERIS42', request.session.session_key, hashlib.sha1
    ).hexdigest()

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
        'user_email': request.session.get('user_email'),
        's3_policy': s3_policy,
        's3_signature': signature,
        'AWS_ACCESS_KEY_ID': settings.AWS_ACCESS_KEY_ID,
        'AWS_S3_BUCKET': settings.AWS_S3_BUCKET,
        'key_prefix': 'gallery/{0}'.format(prefix)
    }
    
    return render_to_response('gallery/index.html', context, context_instance=RequestContext(request))


@require_http_methods(['POST'])
def save_bio(request):
    """ receive AJAX post from class gallery page """

    user_bio = gallery_api.save_bio(
        request.POST['email'],
        request.POST['name'],
        request.POST['bio'],
        request.POST['avatar'],
        request.POST.get('twitter', None)
    )
    
    user_email = request.session.get('user_email', False)
    if user_email and user_email == user_bio['email']:
        user_bio = gallery_api.confirm_bio(user_bio['confirmation_code'])
    else:
        send_confirmation_email(
            user_bio['email'], user_bio['name'], user_bio['avatar'],
            user_bio['bio'], user_bio['confirmation_code']
        )
    
    request.session['user_bio'] = user_bio

    # check if user signed up for the mooc
    try:
        signup_api.get_signup(request.POST['email'])
    except:
        messages.warning(request, 'It looks like you have not signed up for this sequence of the MOOC! We saved your profile, but you still need to sign up.')
        # redirect user to signup page
        return http.HttpResponseRedirect(reverse('home'))

    return http.HttpResponseRedirect(reverse('gallery_gallery'))


def confirm_updates(request, confirmation_code):
    try:
        bio = gallery_api.confirm_bio(confirmation_code)
        request.session['user_bio'] = bio
        request.session['user_email'] = bio['email']
    except Exception:
        messages.error(request, 'Could not find the confirmation code. Please make sure the URL is correct')

    return http.HttpResponseRedirect(reverse('gallery_gallery'))
