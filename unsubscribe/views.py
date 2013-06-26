from django import http
from django.views.decorators.csrf import csrf_exempt

from mailgun import utils
import models as unsubscribe_model

import logging
log = logging.getLogger(__name__)

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

