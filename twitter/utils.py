from django.conf import settings

import hashlib
import hmac
import base64
import urllib
import time
import random
import string
import requests


def get_token():
    url = 'https://api.twitter.com/oauth/request_token'
    resp = authorize_request(
        'POST', url, 
        ('oauth_callback', 'http%3A%2F%2Flocalhost%2Fsign-in-with-twitter%2F'),
    )
    return resp


def authorize_request(method, url, extra_oauth_params, oauth_token=''):
    """ take a Request object and add oauth headers to it """
    nonce = ''.join([random.choice(string.digits + string.letters) for i in range(32)])

    parameter_values = [
        ('oauth_consumer_key', settings.TWITTER_OAUTH_CONSUMER_KEY),
        ('oauth_nonce', nonce),
        ('oauth_signature_method', 'HMAC-SHA1'),
        ('oauth_timestamp', str(int(time.time()))),
        ('oauth_version', '1.0'),
    ]
    if oauth_token:
        parameter_values += [('oauth_token', oauth_token)]
    parameter_values += extra_oauth_params

    signature = get_signature(method, url, parameter_values, oauth_token)
    parameter_values += [
        ('oauth_signature', signature)
    ]
    ff = lambda x: (urllib.quote(x[0], safe=''), urllib.quote(x[1], safe=''))
    parameter_values = map(ff, parameter_values)
    authorization_header = ','.join(
        ["{0}={1}".format(k,v) for k,v in parameter_values]
    )

    r = requests.request(method, url, headers={'Authorization': authorization_header})
    return r


def get_signature(http_method, url, parameter_values, oauth_token_secret=''):

    ff = lambda x: (urllib.quote(x[0], safe=''), urllib.quote(x[1], safe=''))
    parameter_values = map(ff, parameter_values)
    parameter_values.sort(key=lambda x: x[0])
    parameter_string = '&'.join(['{0}={1}'.format(x,y) for x,y in parameter_values])

    signature_base_string = '&'.join([
        http_method.upper(),
        urllib.quote(url, safe=''),
        urllib.quote(parameter_string, safe='')
    ])

    consumer_secret = settings.TWITTER_OAUTH_CONSUMER_SECRET
    signing_key = '&'.join([consumer_secret, oauth_token_secret])

    signature = base64.b64encode(
        hmac.new(
            key=signing_key, 
            msg=signature_base_string, 
            digestmod=hashlib.sha1
        ).digest()
    )

    return signature
