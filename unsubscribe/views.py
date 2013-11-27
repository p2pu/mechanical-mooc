from django import http
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib import messages
from django.core.urlresolvers import reverse

from mailgun import utils
from signup import models as signup_model
from unsubscribe import models as unsubscribe_model
from unsubscribe.emails import send_unsubscribe_confirmation

import logging
log = logging.getLogger(__name__)


def unsubscribe(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            signup = signup_model.get_signup(email)
            send_unsubscribe_confirmation(signup)
            messages.info(request, u'You will shortly receive an email to confirm that you wish to unsubscribe')
            return http.HttpResponseRedirect(reverse('home'))
        except:
            context['error'] = 'Could not find signup.'

    return render_to_response('unsubscribe/unsubscribe.html', context, context_instance=RequestContext(request))


def confirm(request, key):
    try:
        su = signup_model.get_signup_by_invite_code(key)
        unsubscribe_model.unsubscribe_user(su['email'])
        messages.success(request, 'You have been successfully unsubscribed.')
    except:
        log.error(u'Could not find signup for confirmation code {0}'.format(key))
        messages.error(request, 'We could not find the signup that corresponds to the unsubscribe link you used.')
    return http.HttpResponseRedirect(reverse('home'))


@csrf_exempt
def unsubscribe_webhook(request):
    verified = utils.verify_webhook(
        request.POST.get('token'), 
        request.POST.get('timestamp'),
        request.POST.get('signature')
    )

    if not verified:
        return http.HttpResponseForbidden()

    address = request.POST.get('recipient')

    try:
        if request.POST.get('mailing-list'):
            unsubscribe_model.unsubscribe_from_sequence(address)
        else:
            unsubscribe_model.unsubscribe_user(address)
    except:
        log.error(u'Could not unsubscribe {0}')

    return http.HttpResponse('')

