# -*- coding: utf-8 -*-
"""

Api library for Uso bot
By Renondedju and Jamu

"""

import requests
from enum import Enum

import settings


def get_beatmap(key, beatmap_id, session = None):
    """ Fetch a beatmap from bancho api """

    url = "https://osu.ppy.sh/api/get_beatmaps?k={}&b={}".format(key, beatmap_id)
    if (not session):
        return requests.get(url).json()
    else:
        return session.get(url).json()

def get_beatmapset(key, set_id, session = None):
    """ Fetch a beatmapset from bancho api """

    url = "https://osu.ppy.sh/api/get_beatmaps?k={}&s={}".format(key, set_id)
    if (not session):
        return requests.get(url).json()
    else:
        return session.get(url).json()

def get_scores(key, beatmap_id, user, mode, session = None):
    """ Fetch a user score on a given beatmap from bancho api """

    url = "https://osu.ppy.sh/api/get_scores?k={}&u={}&b={}&m={}".format(key, user, beatmap_id, mode)
    if (not session):
        return requests.get(url).json()
    else:
        return session.get(url).json()

def get_user(key, user, mode, session = None):
    """ Fetch user data from bancho api """

    url = "https://osu.ppy.sh/api/get_user?k={}&u={}&m={}".format(key, user, mode)
    if (not session):
        return requests.get(url).json()
    else:
        return session.get(url).json()

def get_user_best(key, user, mode, limit, session = None):
    """ Fetch bests scores for a user from bancho api """

    url = "https://osu.ppy.sh/api/get_user_best?k={}&u={}&m={}&limit={}".format(key, user, mode, limit)
    if (not session):
        return requests.get(url).json()
    else:
        return session.get(url).json()

def get_user_recent(key, user, mode, session = None):
    """ Fetch the recents scores for a user from bancho api """

    url = "https://osu.ppy.sh/api/get_user_recent?k={}&u={}&m={}".format(key, user, mode)
    if (not session):
        return requests.get(url).json()
    else:
        return session.get(url).json()


class ApiError(Exception):
    pass


class Mode(Enum):
    OSU = 0
    TAIKO = 1
    CTB = 2
    MANIA = 3


class Api:
    '''
    bancho api abstraction layer for python

    Returns plain json for now, declare return type classes + serializer
    or maybe simply use github.com/khazhyk/osuapi/ ?
    '''

    api_key = settings.OSU_API_KEY
    api_url = settings.OSU_API_URL

    def __init__(self, session=None, mode=None):
        '''
        can take a session as argument, is that even needed? just reuse Api
        object instead of session
        '''
        self.session = session or requests.session()

    def request(self, endpoint, args):
        print(self.api_url + endpoint, {'k': self.api_key, **args})
        r = self.session.get(self.api_url + endpoint, params={'k': self.api_key, **args})
        if r.ok:
            return r.json()
        raise ApiError(r.reson)  # or something like that

    def get_beatmap_file(self, beatmap_id):
        """ Fetch beatmap file from bancho api """
        r = self.session.get('https://osu.ppy.sh/osu/{}'.format(beatmap_id))
        if r.ok:
            return r.text
        raise ApiError(r.reson)  # or something like that

    def get_beatmap(self, beatmap_id):
        """ Fetch a beatmap from bancho api """
        return self.request('get_beatmaps', {'b': beatmap_id})

    def get_beatmapset(self, set_id):
        """ Fetch a beatmapset from bancho api """
        return self.request('get_beatmaps', {'s': set_id})

    def get_user_bests(self, user_id, mode=None, limit=500):
        """ Fetch a beatmapset from bancho api """
        params = {
            'u': user_id,
            'limit': limit,
        }
        if mode is not None:
            params['m'] = mode.value
        return self.request('get_user_best', params)
