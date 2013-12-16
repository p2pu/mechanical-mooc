from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django import http
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from classphoto import models as classphoto_api
from classphoto.utils import create_s3_policy_doc
from classphoto.emails import send_user_link

from signup import models as signup_api
from sequence import models as sequence_api

import hmac, hashlib
import random


def check_user(method):
    def call_view(*args, **kwargs):
        request = args[0]
        key = request.GET.get('key', None)
        if not key:
            return method(*args, **kwargs)
        try:
            su = signup_api.get_signup_by_invite_code(key)
        except:
            return method(*args, **kwargs)
        request.session['user_email'] = su['email']
        if request.session.get('user_bio'):
            del request.session['user_bio']
        # get the user bio if possible
        try:
            request.session['user_bio'] = classphoto_api.get_bio(su['email'])
        except:
            pass
        return http.HttpResponseRedirect(request.path)
    return call_view


@check_user
def sequence_redirect(request):
    # TODO if we have a signed in user, we should redirect to the right sequence
    current_sequence = sequence_api.get_current_sequence_number()
    if not current_sequence:
        return http.HttpResponseNotFound()
    url = reverse('classphoto_classphoto', kwargs={'sequence':current_sequence})
    return http.HttpResponseRedirect(url)


@check_user
def classphoto(request, sequence):
    """ show classphoto for all signups for this sequence with profiles """
    s3_policy, signature = create_s3_policy_doc(settings.AWS_S3_BUCKET, 'classphoto')

    prefix = hmac.new(
        'THEANSWERIS42', request.session.session_key, hashlib.sha1
    ).hexdigest()

    bios = classphoto_api.get_bios(sequence, limit=0)
    bios += [{'email': ''} for i in range(len(bios), 36)]
    bios = random.sample(bios, 36)

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
        bios[11] = {'email': ''}

    context = {
        'bios': bios,
        'user_bio': user_bio,
        'user_email': request.session.get('user_email'),
        'sequence': sequence,
        's3_policy': s3_policy,
        's3_signature': signature,
        'AWS_ACCESS_KEY_ID': settings.AWS_ACCESS_KEY_ID,
        'AWS_S3_BUCKET': settings.AWS_S3_BUCKET,
        'key_prefix': 'classphoto/{0}'.format(prefix)
    }
    
    return render_to_response('classphoto/index.html', context, context_instance=RequestContext(request))


@require_http_methods(['POST'])
def save_bio(request, sequence):
    """ receive AJAX post from class classphoto page """

    url = reverse('classphoto_classphoto', kwargs={'sequence': sequence})

    # TODO validate data on the server side also!

    # check if user signed up for the mooc
    signed_up = False
    try:
        signup = signup_api.get_signup(request.POST['email'])
        signed_up = True
    except:
        pass

    if not signed_up or signup['sequence'] != int(sequence):
        messages.error(request, 'We couln\'t find your signup. Please check if you just gave us the email you signed up with?')
        #TODO: this error should not be possible
        return http.HttpResponseRedirect(url)

    if request.POST['email'] != request.session.get('user_email'):
        messages.error(request, 'Oops! We don\'t recognize that email. Maybe you signed up with a different one?')
        return http.HttpResponseRedirect(url)

    user_bio = classphoto_api.save_bio(
        request.POST['email'],
        sequence,
        request.POST['name'],
        request.POST['bio'],
        request.POST['avatar'],
        request.POST.get('twitter', None),
        request.POST.get('gplus', None)
    )
    request.session['user_bio'] = user_bio
    
    messages.success(request, 'Sweet! You\'re now in the Class Photo!')

    return http.HttpResponseRedirect(url)


@require_http_methods(['POST'])
def request_link(request):
    signup = None
    try:
        signup = signup_api.get_signup(request.POST.get('email'))
        messages.success(request, 'Check your inbox -- a tasty new link will be there shortly.')
        send_user_link(signup['email'], signup['key'])
    except:
        messages.error(request, 'Not so fast, partner -- you need to sign up for the Mechanical MOOC first!')
    url = reverse('classphoto_sequence_redirect')
    if settings.DEBUG and signup:
        url += '?key={0}'.format(signup['key'])
    return http.HttpResponseRedirect(url)


def clear_session(request):
    if request.session.get('user_bio'):
        del request.session['user_bio']
    if request.session.get('user_email'):
        del request.session['user_email']
    return http.HttpResponseRedirect(reverse('classphoto_sequence_redirect'))
