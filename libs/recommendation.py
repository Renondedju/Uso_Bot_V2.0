# -*- coding: utf-8 -*-
"""

    Beatmap recommendation algorythm (R Algo)
    By Renondedju and Jamu

"""

from __main__ import *

import os
import sys

sys.path.append(os.path.realpath('../'))

from libs.user    import User
from libs.beatmap import Beatmap
from libs.preset  import Preset

import json
import time
import random
import sqlite3

class REngine:
    """ Recommendation engine """

    def __init__(self):
        """ Init """

        self.settings = settings
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

    def get_mods(self, mods_dict):

        choice = self.weighted_choice(zip(mods_dict.keys(), mods_dict.values()))

        if choice == "":
            return ""
        return "_" + choice

    def recommend(self, preset:Preset, count:int):
        """ R Algo """

        connexion = sqlite3.connect(self.database_path)
        cursor = connexion.cursor()

        self.reset_precision()

        self.recommendatons = []
        self.mods           = []
 
        #Beatmaps research loop
        while (len(self.recommendatons) < count):

            mods = self.get_mods(preset.mods)

            #Main beatmap request
            cursor.execute("""SELECT beatmap_id FROM beatmaps WHERE
                 PP_{}{}       BETWEEN ? AND ? AND
                 bpm           BETWEEN ? AND ? AND
                 playstyle     BETWEEN ? AND ? AND
                 hit_length    BETWEEN ? AND ? AND
                 diff_size     BETWEEN ? AND ? AND
                 diff_approach BETWEEN ? AND ? AND
                 diff_overall  BETWEEN ? AND ? AND
                 beatmap_id NOT IN ({})
                 LIMIT 1"""
                 .format(max(preset.acc, 97), 
                         mods, "'00000'" + preset.user.get_recommended(mods)),

                [round(preset.up_pp    * self.down_precision), 
                 round(preset.down_pp  * self.up_percision),
                 round(preset.up_bpm   * self.down_precision),
                 round(preset.down_bpm * self.up_percision),
                 preset.up_playstyle   * self.down_precision,
                 preset.down_playstyle * self.up_percision,
                 preset.up_len         * self.down_precision,
                 preset.down_len       * self.up_percision,
                 preset.up_cs          * self.down_precision,
                 preset.down_cs        * self.up_percision,
                 preset.up_ar          * self.down_precision,
                 preset.down_ar        * self.up_percision,
                 preset.up_od          * self.down_precision,
                 preset.down_od        * self.up_percision,])
            
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
                preset.user.get_recommended(mods, "'" + str(beatmap_id[0]) + "'")

        if (len(self.recommendatons) == count):
            #Saving the users recommendations if everything is fine
            preset.user.save_user_profile()

        return self.recommendatons

if __name__ == '__main__':
    # --- Test lines !

    now = time.time()
    engine = REngine()
    engine.recommend(Preset(User(osu_name = "Renondedju")), 10)
    print("Done, here are the results ({}), {}% of precision".format(len(engine.recommendatons), engine.precision * 100))
    for i in range(10):
        print(engine.recommendatons[i].beatmap_id, end = ' - ')
        print(engine.mods[i])
    print ('Done in {} s'.format(time.time() - now))
