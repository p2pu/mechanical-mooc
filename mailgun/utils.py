from django.conf import settings

import hashlib
import hmac
import datetime

def verify_webhook(token, timestamp, signature):
    """ Check that this callback really comes from mailgun """
    api_key = settings.MAILGUN_API_KEY
    return signature == hmac.new(
        key=api_key,
        msg='{}{}'.format(timestamp, token),
        digestmod=hashlib.sha256).hexdigest()


def parse_timestamp(timestamp_text):
     return datetime.datetime.strptime(timestamp_text, '%a, %d %b %Y %H:%M:%S GMT')
