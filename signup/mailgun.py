import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings

def call_mailgun(method, api_sub_url, data):
    api_url = '/'.join([settings.MAILGUN_API_URL.strip('/'), api_sub_url.strip('/')])
    auth = HTTPBasicAuth('api', settings.MAILGUN_API_KEY)
    return requests.request(method, api_url, auth=auth, data=data)


def send_email(to_email, from_email, subject, text_body, html_body=None):
    post_data = {
        'from': from_email,
        'to': to_email,
        'subject': subject,
        'text': text_body
    }
    if html_body:
        data['html'] = html_body
    sub_url = '/'.join([settings.MAILGUN_API_DOMAIN, 'messages'])
    resp = call_mailgun('POST', sub_url, post_data)
    if resp.status_code != 200:
        raise Exception(resp.text)


def create_list(address, name=None, description=None, access_level=None):
    data = {
        'address': address,
    }
    if name:
        data['name'] = name
    if description:
        data['description'] = description
    if access_level:
        if access_level not in ['readonly', 'members', 'everyone']:
            raise Exception('Invalid access level')
        data['access_level'] = access_level

    resp = call_mailgun('POST', 'lists', data)
    if resp.status_code != 200:
        raise Exception(resp.text)


def add_list_member(list_address, member_address):
    data = {
        'address': member_address,
        'upsert': 'yes',
    }
    resp = call_mailgun('POST', 'lists/{address}/members'.format(address=list_address), data)
    if resp.status_code != 200:
        raise Exception(resp.text)



def remove_list_member(list_address, member_address):
    resp = call_mailgun(
        'DELETE', 
        'lists/{address}/members/{member_address}'.format(address=list_address, member_address=member_address),
        {}
    )
    if resp.status_code != 200:
        raise Exception(resp.text)


