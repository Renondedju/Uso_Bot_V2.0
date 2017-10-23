# -*- coding: utf-8 -*-

import json
import sqlite3

from user    import User
from beatmap import Beatmap

class REngine:

    def __init__(self):

        self.settings = json.loads(open('../config.json', 'r').read())
        self.database_path = self.settings['database_path']

        #Just a simple container
        self.recommendatons = []

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

        print("extend_research()")

        return

    def select_mod(user:User):
        """ Selecting a random mod """

        mods_chance = (user.Nomod_playrate,
                       user.HR_playrate,
                       user.HD_playrate
                       user.DT_playrate,
                       user.DTHD_playrate,
                       user.DTHR_playrate,
                       user.HRHD_playrate,
                       user.DTHRHD_playrate)

        mods_name  = ("", "_HR", "_HD", "_DT", "_DTHD", "_DTHR", "_HRHD", "_DTHRHD")
        dictionary = dict(zip(mods_name, mods_chance))

        return random.choice([k for k in dictionary for dummy in range(dictionary[k])])

    def recommend(self, user:User, count:int):
        """ R Algo """

        connexion = sqlite3.connect(self.database_path)
        cursor = connexion.cursor()

        self.reset_precision()

        self.recommendatons = []
        beatmap_ids = []
 
        #Beatmaps research loop
        while (len(beatmap_ids) < count):

            mods = self.select_mod(user)

            cursor.execute("""SELECT beatmap_id FROM beatmaps WHERE
                 PP_100{} BETWEEN ? AND ? LIMIT ?""".format(mods),

                [user.pp_average * self.up_percision,
                 user.pp_average * self.down_precision,
                 count,])
            
            beatmap_ids = cursor.fetchall()

            # If we don't have all the beatmaps we want, precision goes down by 1%
            # And retrying
            self.extend_research()

        for id in beatmap_ids:
            self.recommendatons.append(Beatmap(id[0]))

        return self.recommendatons

if __name__ == '__main__':
    # --- Test lines !

    engine = REngine()
    engine.recommend(User(7418575), 2)
    print("Done, here are the results ({}), {}% of precision".format(len(engine.recommendatons), engine.precision * 100))