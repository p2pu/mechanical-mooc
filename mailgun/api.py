import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
import django.utils.simplejson as json

def call_mailgun(method, api_sub_url, data):
    api_url = '/'.join([settings.MAILGUN_API_URL.strip('/'), api_sub_url.strip('/')])
    auth = HTTPBasicAuth('api', settings.MAILGUN_API_KEY)
    return requests.request(method, api_url, auth=auth, data=data)


def send_email(to_email, from_email, subject, text_body, html_body=None, tags=None):
    return send_mass_email(
        [to_email],
        from_email,
        subject,
        text_body,
        html_body=None,
        tags=None
    )


def send_mass_email(to_emails, from_email, subject, text_body, html_body=None, tags=None):
    """ send email to multiple users, but each being to only one in the to field """
    post_data = [
        ('from', from_email),
        ('subject', subject),
        ('text', text_body),
        ('o:tracking', 'yes'),
        ('o:tracking-clicks', 'yes'),
        ('o:tracking-opens', 'yes'),
    ]

    post_data += [ ('to', to_email) for to_email in to_emails ]
    post_data += [ ('recipient-variables', [json.dumps({to_email:{}}) for to_email in to_emails] ) ]

    if html_body:
        post_data += [('html', html_body),]
 
    if tags:
        post_data += [ ("o:tag", tag) for tag in tags]

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


def get_list(list_address):
    resp = call_mailgun(
        'GET',
        'lists/{address}'.format(address=list_address),
        {}
    )
    if resp.status_code == 404:
        return None
    if resp.status_code != 200:
        raise Exception(resp.text)
    return resp.json()


def get_list_members(list_address):
    resp = call_mailgun(
        'GET',
        'lists/{address}/members'.format(address=list_address),
        {}
    )
    if resp.status_code != 200:
        raise Exception(resp.text)
    return resp.json()['items']
