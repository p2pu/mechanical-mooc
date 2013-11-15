from django.conf import settings

from signup import models

from pyechonest import config
from pyechonest import catalog

import requests
import time
from collections import Counter


def create_taste_profiles_for_sequence(sequence):
    signups = models.get_signups(sequence)
    create_taste_profiles(signups)


def create_taste_profiles(signups):
    """ Create EchoNest taste profiles for every signup in a sequence """

    config.ECHO_NEST_API_KEY = settings.ECHONEST_API_KEY
    for signup_index, signup in enumerate(signups):
        artists = list(set([ signup['questions'].get('artist{0}'.format(i)) for i in range(1,6) ]))
        artists.sort()
        print("Updating profile {0} of {1}".format(signup_index+1, len(signups)))
        taste_profile = None
        try:
            taste_profile = catalog.get_catalog_by_name(signup['email'])
        except:
            pass
        if not taste_profile:
            taste_profile = catalog.create_catalog_by_name(signup['email'], 'artist')
        items = []
        for i, artist in enumerate(artists):
            item = {
                'item_id': u'{0}-{1}'.format(signup['email'], i),
                'artist_name': artist,
                'favorite': True
            }
            items += [{'action': 'update', 'item': item}]
            
        taste_profile.update(items)
        time.sleep(60/40.0)


def get_sequence_scores(sequence):
    """ Build a dictionary with the distances between all taste profiles """
    """
    { 
        '<profile_id>': {'name': '<profile_name>', 'suggest': {'<profile_id>': <score>, '<profile_id>': <score>, ...} },
        '<profile_id>': {'name': '<profile_name>', 'suggest': {'<profile_id>': <score>, '<profile_id>': <score>, ...} },
        ...
        '<profile_id>': {'name': '<profile_name>', 'suggest': {'<profile_id>': <score>, '<profile_id>': <score>, ...} },
    }
    """

    config.ECHO_NEST_API_KEY = settings.ECHONEST_API_KEY
    url = 'http://developer.echonest.com/api/v4/catalog/similar'

    signups = models.get_signups(sequence)
    similar_results = {}
    for i, signup in enumerate(signups):
        print("Fetching taste profile {0} of {1}".format(i, len(signups)))
        # TODO: are we sure the taste profile exists?
        taste_profile = catalog.get_catalog_by_name(signup['email'])
        params = {
            'api_key': settings.ECHONEST_API_KEY,
            'id': taste_profile.id,
            'results': 40
        }
        resp = requests.get(url, params=params)
        profile_scores = {}
        for profile in resp.json()['response'].get('catalogs', []):
            profile_scores[profile['id']] = profile['score']
        similar_results[taste_profile.id] = {'name': signup['email'], 'suggest': profile_scores}

    return similar_results


def get_signup_artists(email):
    signup = models.get_signup(email)
    return [ signup['questions'].get('artist{0}'.format(i)) for i in range(1,6) ]


def get_group_artists(group_profiles, data):
    artists = Counter()
    for profile in group_profiles:
        signup = models.get_signup(data[profile]['name'])
        for artist in [ signup['questions'].get('artist{0}'.format(i)) for i in range(1,6) ]:
            artists[artist] += 1
    return artists
