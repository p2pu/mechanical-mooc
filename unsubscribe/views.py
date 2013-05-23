from django import http
from mailgun import utils

import models as unsubscribe_model

def unsubscribe_webhook(request):
    verified = utils.verify_webhook(
        request.POST.get('token'), 
        request.POST.get('timestamp'),
        request.POST.get('signature')
    )

    if not verified:
        return http.HttpResponseForbidden()

    address = request.POST.get('recipient')

    if request.POST.get('mailing-list'):
        unsubscribe_model.unsubscribe_from_sequence(address)
    else:
        unsubscribe_model.unsubscribe_completely(address)

