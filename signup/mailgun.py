import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings

def send_email(to_email, from_email, subject, text_body, html_body=None):
    api_url = '{0}/messages/'.format(settings.MAILGUN_API_DOMAIN)
    auth = ('api', settings.MAILGUN_API_KEY)
    post_data = {
        'from': from_email,
        'to': to_email,
        'subject': subject,
        'text': text_body
    }
    if html_body:
        data['html'] = html_body
    resp = requests.post(api_url, auth=HTTPBasicAuth(auth[0], auth[1]), data=post_data)
    #TODO check response code

