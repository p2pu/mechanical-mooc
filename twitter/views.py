from django import http
from twitter import utils

def get_data(request):
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

