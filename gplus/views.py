from django import http
from django.conf import settings
from django.views.decorators.http import require_http_methods

import json
import requests
import re


def get_google_user_id(profile_url):
    m = re.match('.*plus.google.com.*/(?P<user_id>[\d]+).*', profile_url)
    try:
        user_id = m.group('user_id')
    except:
        raise Exception('Could not determine user ID')
    return user_id


@require_http_methods(['POST'])
def get_profile(request):
    if 'profile_url' not in request.POST.keys():
        return http.HttpResponseServerError()

    profile_url = request.POST.get('profile_url')

    API_URL = 'https://www.googleapis.com/plus/v1/people/{user_id}?key={api_key}'
    try:
        user_id = get_google_user_id(profile_url)
        resp = requests.get(API_URL.format(user_id=user_id, api_key=settings.GOOGLE_PLUS_API_KEY))
        if resp.status_code != 200:
            raise Exception('Could not fetch data from Google plus API for user {0}'.format(user_id))
        profile_data = {
            'avatar': resp.json()['image']['url'],
            'name': resp.json()['displayName'],
            'bio': resp.json().get('aboutMe', '')
        }
        profile_data['avatar'] = re.sub('\?sz=[\d]+', '?sz=120', profile_data['avatar'])
        return http.HttpResponse(json.dumps(profile_data))
    except:
        return http.HttpResponseNotFound()
