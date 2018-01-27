# -*- coding: utf-8 -*-
"""

	Api library for Uso bot
	By Renondedju and Jamu

"""

import requests

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
