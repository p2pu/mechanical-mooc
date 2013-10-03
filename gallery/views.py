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
from gallery.emails import send_user_link

from signup import models as signup_api
from sequence import models as sequence_api

import hmac, hashlib
import random


def check_user(method):
    def call_view(*args, **kwargs):
        request = args[0]
        key = request.GET.get('key', None)
        if key:
            su = signup_api.get_signup_by_invite_code(key)
            request.session['user_email'] = su['email']
            # TODO rather get the user bio if possible
            if request.session.get('user_bio'):
                del request.session['user_bio']
            return http.HttpResponseRedirect(request.path)
        return method(*args, **kwargs)
    return call_view


@check_user
def sequence_redirect(request):
    #TODO handle None returned from get_current_sequence when there is no sequence
    # TODO if we have a signed in user, we should redirect to the right sequence
    current_sequence = sequence_api.get_current_sequence_number()
    url = reverse('gallery_gallery', kwargs={'sequence':current_sequence})
    return http.HttpResponseRedirect(url)


@check_user
def gallery(request, sequence):
    """ show gallery for all signups for this sequence with profiles """
    s3_policy, signature = create_s3_policy_doc(settings.AWS_S3_BUCKET, 'gallery')

    prefix = hmac.new(
        'THEANSWERIS42', request.session.session_key, hashlib.sha1
    ).hexdigest()

    bios = gallery_api.get_bios(sequence, limit=32)
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
        'sequence': sequence,
        's3_policy': s3_policy,
        's3_signature': signature,
        'AWS_ACCESS_KEY_ID': settings.AWS_ACCESS_KEY_ID,
        'AWS_S3_BUCKET': settings.AWS_S3_BUCKET,
        'key_prefix': 'gallery/{0}'.format(prefix)
    }
    
    return render_to_response('gallery/index.html', context, context_instance=RequestContext(request))


@require_http_methods(['POST'])
def save_bio(request, sequence):
    """ receive AJAX post from class gallery page """

    # check if user signed up for the mooc
    signed_up = False
    try:
        signup = signup_api.get_signup(request.POST['email'])
        signed_up = True
    except:
        pass

    if not signed_up or signup['sequence'] != int(sequence):
        messages.warning(request, 'It looks like you did not sign up for this instance of the MOOC! You can sign up for the next time the MOOC runs.')
        # redirect user to signup page
        return http.HttpResponseRedirect(reverse('home'))

    user_bio = gallery_api.save_bio(
        request.POST['email'],
        sequence,
        request.POST['name'],
        request.POST['bio'],
        request.POST['avatar'],
        request.POST.get('twitter', None)
    )
    
    user_email = request.session.get('user_email', False)
    if user_email and user_email == user_bio['email']:
        user_bio = gallery_api.confirm_bio(user_bio['confirmation_code'])
        messages.success(request, 'Your information has been updated.')
    else:
        send_confirmation_email(
            user_bio['email'], user_bio['name'], user_bio['avatar'],
            user_bio['bio'], user_bio['confirmation_code']
        )
        messages.success(request, 'Your information has been updated, you will shortly receive an email to confirm that you made the updates yourself.')
    
    request.session['user_bio'] = user_bio

    url = reverse('gallery_gallery', kwargs={'sequence': sequence})
    return http.HttpResponseRedirect(url)


def confirm_updates(request, confirmation_code):
    try:
        bio = gallery_api.confirm_bio(confirmation_code)
        request.session['user_bio'] = bio
        request.session['user_email'] = bio['email']
    except Exception:
        messages.error(request, 'Could not find the confirmation code. Please make sure the URL is correct')
    
    url = reverse('gallery_gallery', kwargs={'sequence': bio['sequence']})
    return http.HttpResponseRedirect(url)


@require_http_methods(['POST'])
def request_link(request):
    signup = signup_api.get_signup(request.POST.get('email'))
    if settings.DEBUG:
        url = reverse('gallery_sequence_redirect')
        url += '?key={0}'.format(signup['key'])
    send_user_link(signup['email'], signup['key'])
    messages.success(request, 'You will shortly receive an email with a link to update your picture')
    return http.HttpResponseRedirect(url)


def clear_session(request):
    if request.session.get('user_bio'):
        del request.session['user_bio']
    if request.session.get('user_email'):
        del request.session['user_email']
    return http.HttpResponseRedirect(reverse('gallery_sequence_redirect'))
