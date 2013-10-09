from django import http
from django.conf import settings
from django.views.decorators.http import require_http_methods

import json

from twitter import utils

@require_http_methods(['POST'])
def get_data(request):
    if 'twitter_handle' not in request.POST.keys():
        return http.HttpResponseServerError()

    twitter_handle = request.POST.get('twitter_handle')
    creds = (settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
    try: 
        user_data = utils.get_user_data(twitter_handle, creds)
        bio_data = {
            'avatar': user_data['profile_image_url'],
            'name': user_data['name'],
            'bio': user_data['description']
        }
        if '_normal' in bio_data['avatar']:
            bio_data['avatar'] = bio_data['avatar'].replace('_normal', '')
        return http.HttpResponse(json.dumps(bio_data))
    except:
        return http.HttpResponseNotFound()


def old(request):
    request_token_dict = utils.get_request_token()
    request.session['oauth_token'] = request_token_dict['oauth_token']
    request.session['oauth_token_secret'] = request_token_dict['oauth_token_secret']
    redirect_url = 'https://api.twitter.com/oauth/authenticate?oauth_token={0}'.format(
        request_token_dict['oauth_token']
    )
    return http.HttpResponseRedirect(redirect_url)


def oauth_callback(request):
    oauth_token = request.GET.get('oauth_token')
    oauth_verifier = request.GET.get('oauth_verifier')

    oauth_token_secret = request.session['oauth_token_secret']
    access_token_dict = utils.get_access_token(oauth_verifier, (oauth_token, oauth_token_secret))
    
    user = utils.get_user_data(
        access_token_dict['screen_name'],
        (access_token_dict['oauth_token'], access_token_dict['oauth_token_secret'])
    )
    raise Exception()

