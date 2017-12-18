# -*- coding: utf-8 -*-
"""

    Beatmap recommendation algorythm (R Algo)
    By Renondedju and Jamu

"""

import os
import sys

sys.path.append(os.path.realpath('../'))

from libs.user    import User
from libs.beatmap import Beatmap
from libs.preset  import Preset

import json
import random
import sqlite3

class REngine:
    """ Recommendation engine """

    def __init__(self):
        """ Init """

        self.settings = json.loads(open('../config.json', 'r').read())
        self.database_path = self.settings['database_path']

        # Mod selection
        self.weighted_choice = lambda s : random.choice(sum(([v]*int(wt) for v,wt in s),[]))

        #Just a simple container
        self.recommendatons = []
        self.mods           = []

        self.precision      = 1.0
        self.up_percision   = 1.0
        self.down_precision = 1.0

    def reset_precision(self):
        """ Reseting presision for a new recommendation """

        self.precision      = 1.0
        self.up_percision   = 1.0
        self.down_precision = 1.0

    def extend_research(self):
        """ Decreasing precision to get enought maps """

        self.precision      -= 0.01
        self.up_percision   += 0.01
        self.down_precision -= 0.01

        if self.down_precision <= 0.0:
            self.down_precision = 0.0
            self.precision      = 0.0

    def select_mod(self, user:User):
        """ Selecting a random mod """

        mods_chance = (user.Nomod_playrate,
                       user.HR_playrate,
                       user.HD_playrate,
                       user.DT_playrate,
                       user.DTHD_playrate,
                       user.DTHR_playrate,
                       user.HRHD_playrate,
                       user.DTHRHD_playrate)

        mods_name  = ("", "_HR", "_HD", "_DT", "_DTHD", "_DTHR", "_HRHD", "_DTHRHD")
        dictionary = zip(mods_name, mods_chance)

        return self.weighted_choice(dictionary)

    def recommend(self, user:User, count:int):
        """ R Algo """

        connexion = sqlite3.connect(self.database_path)
        cursor = connexion.cursor()

        self.reset_precision()

        self.recommendatons = []
        self.mods           = []
 
        #Beatmaps research loop
        while (len(self.recommendatons) < count):

            mods = self.select_mod(user)

            #Main beatmap request
            cursor.execute("""SELECT beatmap_id FROM beatmaps WHERE
                 PP_{}{}    BETWEEN ? AND ? AND
                 bpm        BETWEEN ? AND ? AND
                 beatmap_id NOT IN ({})
                 LIMIT 1"""
                 .format(max(user.accuracy_average, 97), 
                         mods, "'00000'" + user.get_recommended(mods)),

                [round(user.pp_average  * self.down_precision), 
                 round(user.pp_average  * self.up_percision),
                 round(user.bpm_average * self.down_precision),
                 round(user.bpm_average * self.up_percision),])
            
            beatmap_id = cursor.fetchone()

            if (not beatmap_id):
                # If we don't have all the beatmaps we want, precision goes down by 1%
                # And retrying
                self.extend_research()

                if self.precision == 0.0:
                    self.precision = 0.0
                    break #Failed to find any beatmap
            else:
                self.recommendatons.append(Beatmap(beatmap_id[0]))
                self.mods.append(mods.replace('_', ''))
                #Saving the recommendation into the user profile
                user.get_recommended(mods, "'" + str(beatmap_id[0]) + "'")

        if (len(self.recommendatons) == count):
            #Saving the users recommendations if everything is fine
            user.save_user_profile()

        return self.recommendatons

if __name__ == '__main__':
    # --- Test lines !

    engine = REngine()
    engine.recommend(User(7418575), 10)
    print("Done, here are the results ({}), {}% of precision".format(len(engine.recommendatons), engine.precision * 100))
    for i in range(10):
        print(engine.recommendatons[i].beatmap_id, end = ' - ')
        print(engine.mods[i])
