from django.conf import settings

from signup import models

from pyechonest import config
from pyechonest import catalog

import requests
import time
from collections import Counter


def create_taste_profiles(sequence):
    """ Create EchoNest taste profiles for every signup in a sequence """

    config.ECHO_NEST_API_KEY = settings.ECHONEST_API_KEY
    signups = models.get_signups(sequence)
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


def score(profile1, profile2, cache):
    """ Calculate the score from profile1 to profile2 """
    # Note: score(x,y) != score(y,x) from the API
    # so we calculate rscore(x,y) = score(x,y) + score(y,x) 
    # so that rscore(x,y) == rscore(y,x)

    score = 0
    if profile1 in cache:
        if profile2 in cache[profile1]['suggest']:
            score = cache[profile1]['suggest'][profile2]

    if profile2 in cache:
        if profile1 in cache[profile2]['suggest']:
            score += cache[profile2]['suggest'][profile1]

    return score


def group_score(profile, group_profiles, data):
    """ calculate the total score for a profile in a group """
    return sum(map(lambda x: score(x,profile,data), group_profiles))


def get_group_artists(group_profiles, data):
    artists = Counter()
    for profile in group_profiles:
        signup = models.get_signup(data[profile]['name'])
        for artist in [ signup['questions'].get('artist{0}'.format(i)) for i in range(1,6) ]:
            artists[artist] += 1
    return artists


def ckmeans(sequence):
    group_size = 40
    #data = get_sequence_scores(sequence)
    f = open('echonest-data-2013-10-29.json', 'r')
    import json
    data = json.load(f)
    f.close()
    groups = [ {profile: 0 for profile in data.keys()[i:i+group_size]} for i in range(0,len(data.keys()),group_size) ]
    import random
    groups = random.sample(groups, len(groups))
    
    def update_groups():
        for gn, group in enumerate(groups):
            for profile in group:
                group[profile] = group_score(profile, [p for p in group if p != profile], data)
            #print('Group {0} Total = {1}'.format(gn, sum(group.values())))
            #print('Artist: {0}'.format({k:v for k,v in get_group_artists(group.keys(), data).items() if v > 1 }))
        group_sums = [sum(group.values()) for group in groups]
        print("{0} {1}".format(sum(group_sums), group_sums))
    update_groups()

    for bb in range(10):
        for gn, group in enumerate(groups):
            for profile in group:
                # calculate a group score for profile in all other groups
                group_scores = [group_score(profile, g, data) for g in groups if g != group ]
                # check if another group has a higher score
                best_score = max(group_scores)
                bgi = group_scores.index(best_score)
                if bgi != gn:
                    # find weakest element in other group
                    worst_profile, worst_score = reduce(lambda x,y: x if x[1] < y[1] else y, groups[bgi].items())
                    # calculate score for worse_profile in different group
                    new_score = group_score(worst_profile, [p for p in group if p != profile], data)
                    if new_score + best_score > group[profile] + groups[bgi][worst_profile]:
                        # do swap
                        del group[profile]
                        group[worst_profile] = new_score
                        del groups[bgi][worst_profile]
                        groups[bgi][profile] = best_score
                        #NOTE: not true the score since we remove the worst element. This may have undesireable effects
        
        update_groups()

    for group in groups:
        print('Artist: {0}'.format({k:v for k,v in get_group_artists(group.keys(), data).items() if v > 1 }))
           
