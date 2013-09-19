from django.conf import settings

import hashlib
import hmac
import base64
import urllib
import time
import random
import string
import requests


def _parse_response(text):
    return dict( [(k[0], k[1]) for k in [i.split('=') for i in text.split('&')]] )


def get_request_token():
    url = 'https://api.twitter.com/oauth/request_token'
    callback = 'http://mooc-signup-test.herokuapp.com/twitter/oauth_callback/'
    resp = authorize_request(
        'POST', url, extra_oauth_params=[('oauth_callback', callback)]
    )
    if resp.status_code != 200:
        raise Exception('Could not get twitter request token')
    return _parse_response(resp.text)


def get_access_token(oauth_verifier, oauth_token_pair):
    url = 'https://api.twitter.com/oauth/access_token'
    body_data = [('oauth_verifier', oauth_verifier)]
    resp = authorize_request('POST', url, [], [], oauth_token_pair, body_data)
    return _parse_response(resp.text)


def get_user_data(screen_name, oauth_token_pair):
    url = 'https://api.twitter.com/1.1/users/show.json'
    resp = authorize_request('GET', url,
        param_data=[('screen_name', screen_name)],
        oauth_token_pair=oauth_token_pair
    )
    return resp


def authorize_request(method, url, param_data=None, extra_oauth_params=None, oauth_token_pair=None, body_data=None):
    """ take a Request object and add oauth headers to it """
    nonce = ''.join([random.choice(string.digits + string.letters) for i in range(32)])

    parameter_values = [
        ('oauth_consumer_key', settings.TWITTER_OAUTH_CONSUMER_KEY),
        ('oauth_nonce', nonce),
        ('oauth_signature_method', 'HMAC-SHA1'),
        ('oauth_timestamp', str(int(time.time()))),
        ('oauth_version', '1.0'),
    ]
    if oauth_token_pair:
        parameter_values += [('oauth_token', oauth_token_pair[0])]
    if extra_oauth_params:
        parameter_values += extra_oauth_params

    signature_parameters = parameter_values
    if param_data:
        signature_parameters = param_data + parameter_values
    if body_data:
        signature_parameters += body_data

    oauth_token_secret = ''
    if oauth_token_pair:
        oauth_token_secret = oauth_token_pair[1]
    signature = get_signature(method, url, signature_parameters, oauth_token_secret)
    parameter_values += [
        ('oauth_signature', signature)
    ]
    ff = lambda x: (urllib.quote(x[0], safe=''), urllib.quote(x[1], safe=''))
    parameter_values = map(ff, parameter_values)
    parameter_values.sort(key=lambda x: x[0])
    authorization_header = ', '.join(
        ['{0}="{1}"'.format(k,v) for k,v in parameter_values]
    )
    authorization_header = "OAuth {0}".format(authorization_header)
    data = None
    if body_data:
        data = '{0}={1}'.format(body_data[0][0], body_data[0][1])
    params = None
    if param_data:
        params = dict(param_data)

    r = requests.request(method, url,
        headers={'Authorization': authorization_header},
        data=data,
        params=params
    )
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
