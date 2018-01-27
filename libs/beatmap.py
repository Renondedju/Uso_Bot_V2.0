# -*- coding: utf-8 -*-
"""
    Beatmap library for uso bot
    By Renondedju and Jamu
"""

import os
import io
import sys
import json
import sqlite3
import requests

sys.path.append(os.path.realpath('../'))

from libs        import pyttanko
from libs.mods   import Mods
from libs.osuapi import get_beatmap

class Beatmap():
    """ Beatmaps class """

    def __init__(self, beatmap_id: int, session = None):
        """ Init """

        #Session : used to signignificaly improve api requests speed
        self.session = session

        #path for later
        self.settings       = json.loads(open('../config.json', 'r').read())
        self.database_path  = self.settings['database_path']
        self.beatmaps_path  = self.settings['beatmap_cache']

        self.beatmaps_str   = ""

        self.beatmap_id     = beatmap_id
        self.uso_id         = 0
        self.beatmapset_id  = 0

        self.bpm                = 0
        self.difficultyrating   = 0
        self.aim_stars          = 0
        self.speed_stars        = 0

        self.playstyle          = 0.5 # 0 = aim (jumps) , 1 = speed (stream)

        self.diff_size      = 0
        self.diff_overall   = 0
        self.diff_approach  = 0
        self.diff_drain     = 0
        self.hit_length     = 0
        self.total_length   = 0
        self.max_combo      = 0

        self.artist         = None
        self.creator        = None
        self.title          = None
        self.version        = None
        self.mode           = 0
        self.tags           = None
        self.approved       = None
        self.approved_date  = None
        self.last_update    = None

        self.PP_100         = 0
        self.PP_100_HR      = 0
        self.PP_100_HD      = 0
        self.PP_100_DT      = 0
        self.PP_100_DTHD    = 0
        self.PP_100_DTHR    = 0
        self.PP_100_HRHD    = 0
        self.PP_100_DTHRHD  = 0

        self.PP_99          = 0
        self.PP_99_HR       = 0
        self.PP_99_HD       = 0
        self.PP_99_DT       = 0
        self.PP_99_DTHD     = 0
        self.PP_99_DTHR     = 0
        self.PP_99_HRHD     = 0
        self.PP_99_DTHRHD   = 0

        self.PP_98          = 0
        self.PP_98_HR       = 0
        self.PP_98_HD       = 0
        self.PP_98_DT       = 0
        self.PP_98_DTHD     = 0
        self.PP_98_DTHR     = 0
        self.PP_98_HRHD     = 0
        self.PP_98_DTHRHD   = 0

        self.PP_97          = 0
        self.PP_97_HR       = 0
        self.PP_97_HD       = 0
        self.PP_97_DT       = 0
        self.PP_97_DTHD     = 0
        self.PP_97_DTHR     = 0
        self.PP_97_HRHD     = 0
        self.PP_97_DTHRHD   = 0

        self.load_beatmap()

    def load_beatmap(self):
        """ Loading a beatmap from the database """

        if not self.beatmap_id or not self.database_path:
            return

        connexion = sqlite3.connect(self.database_path)
        cursor    = connexion.cursor()

        query = cursor.execute("SELECT * FROM beatmaps WHERE beatmap_id = ?", [self.beatmap_id,])

        colname     = [ d[0] for d in query.description ]
        result_list = [ dict(zip(colname, r)) for r in query.fetchall()]
        
        if len(result_list) == 0:
            connexion.close()
            self.import_beatmap()
            self.save_beatmap()
            return #No coresponding beatmap

        self.uso_id         = result_list[0]['uso_id']
        self.beatmapset_id  = result_list[0]['beatmapset_id']

        self.bpm                = result_list[0]['bpm']
        self.difficultyrating   = result_list[0]['difficultyrating']
        self.aim_stars          = result_list[0]['aim_stars']
        self.speed_stars        = result_list[0]['speed_stars']

        if (self.difficultyrating == 0):
            self.playstyle = 0.5
        else:
            self.playstyle = self.speed_stars/self.difficultyrating

        self.diff_size      = result_list[0]['diff_size']
        self.diff_overall   = result_list[0]['diff_overall']
        self.diff_approach  = result_list[0]['diff_approach']
        self.diff_drain     = result_list[0]['diff_drain']
        self.hit_length     = result_list[0]['hit_length']
        self.total_length   = result_list[0]['total_length']
        self.max_combo      = result_list[0]['max_combo']

        self.artist         = result_list[0]['artist']
        self.creator        = result_list[0]['creator']
        self.title          = result_list[0]['title']
        self.version        = result_list[0]['version']
        self.mode           = result_list[0]['mode']
        self.tags           = result_list[0]['tags']
        self.approved       = result_list[0]['approved']
        self.approved_date  = result_list[0]['approved_date']
        self.last_update    = result_list[0]['last_update']

        self.PP_100         = result_list[0]['PP_100']
        self.PP_100_HR      = result_list[0]['PP_100_HR']
        self.PP_100_HD      = result_list[0]['PP_100_HD']
        self.PP_100_DT      = result_list[0]['PP_100_DT']
        self.PP_100_DTHD    = result_list[0]['PP_100_DTHD']
        self.PP_100_DTHR    = result_list[0]['PP_100_DTHR']
        self.PP_100_HRHD    = result_list[0]['PP_100_HRHD']
        self.PP_100_DTHRHD  = result_list[0]['PP_100_DTHRHD']

        self.PP_99          = result_list[0]['PP_99']
        self.PP_99_HR       = result_list[0]['PP_99_HR']
        self.PP_99_HD       = result_list[0]['PP_99_HD']
        self.PP_99_DT       = result_list[0]['PP_99_DT']
        self.PP_99_DTHD     = result_list[0]['PP_99_DTHD']
        self.PP_99_DTHR     = result_list[0]['PP_99_DTHR']
        self.PP_99_HRHD     = result_list[0]['PP_99_HRHD']
        self.PP_99_DTHRHD   = result_list[0]['PP_99_DTHRHD']

        self.PP_98          = result_list[0]['PP_98']
        self.PP_98_HR       = result_list[0]['PP_98_HR']
        self.PP_98_HD       = result_list[0]['PP_98_HD']
        self.PP_98_DT       = result_list[0]['PP_98_DT']
        self.PP_98_DTHD     = result_list[0]['PP_98_DTHD']
        self.PP_98_DTHR     = result_list[0]['PP_98_DTHR']
        self.PP_98_HRHD     = result_list[0]['PP_98_HRHD']
        self.PP_98_DTHRHD   = result_list[0]['PP_98_DTHRHD']

        self.PP_97          = result_list[0]['PP_97']
        self.PP_97_HR       = result_list[0]['PP_97_HR']
        self.PP_97_HD       = result_list[0]['PP_97_HD']
        self.PP_97_DT       = result_list[0]['PP_97_DT']
        self.PP_97_DTHD     = result_list[0]['PP_97_DTHD']
        self.PP_97_DTHR     = result_list[0]['PP_97_DTHR']
        self.PP_97_HRHD     = result_list[0]['PP_97_HRHD']
        self.PP_97_DTHRHD   = result_list[0]['PP_97_DTHRHD']

        connexion.close()

        return

    def save_beatmap(self):
        """ Saves a beatmap into a given database """

        if not self.beatmap_id or not self.database_path:
            return

        connexion = sqlite3.connect(self.database_path)
        cursor = connexion.cursor()

        data = [self.beatmapset_id,
            self.bpm,
            self.difficultyrating,
            self.aim_stars,
            self.speed_stars,
            self.playstyle,
            self.diff_size,
            self.diff_overall,
            self.diff_approach,
            self.diff_drain,
            self.hit_length,
            self.total_length,
            self.max_combo,
            self.artist,
            self.creator,
            self.title,
            self.version,
            self.mode,
            self.tags,
            self.approved,
            self.approved_date,
            self.last_update,
            self.PP_100,
            self.PP_100_HR,
            self.PP_100_HD,
            self.PP_100_DT,
            self.PP_100_DTHD,
            self.PP_100_DTHR,
            self.PP_100_HRHD,
            self.PP_100_DTHRHD,
            self.PP_99,
            self.PP_99_HR,
            self.PP_99_HD,
            self.PP_99_DT,
            self.PP_99_DTHD,
            self.PP_99_DTHR,
            self.PP_99_HRHD,
            self.PP_99_DTHRHD,
            self.PP_98,
            self.PP_98_HR,
            self.PP_98_HD,
            self.PP_98_DT,
            self.PP_98_DTHD,
            self.PP_98_DTHR,
            self.PP_98_HRHD,
            self.PP_98_DTHRHD,
            self.PP_97,
            self.PP_97_HR,
            self.PP_97_HD,
            self.PP_97_DT,
            self.PP_97_DTHD,
            self.PP_97_DTHR,
            self.PP_97_HRHD,
            self.PP_97_DTHRHD,
            self.beatmap_id,]

        try:
            cursor.execute(""" INSERT OR REPLACE INTO beatmaps
            (beatmapset_id,
            bpm,
            difficultyrating,
            aim_stars,
            speed_stars,
            playstyle,
            diff_size,
            diff_overall,
            diff_approach,
            diff_drain,
            hit_length,
            total_length,
            max_combo,
            artist,
            creator,
            title,
            version,
            mode,
            tags,
            approved,
            approved_date,
            last_update,
            PP_100,
            PP_100_HR,
            PP_100_HD,
            PP_100_DT,
            PP_100_DTHD,
            PP_100_DTHR,
            PP_100_HRHD,
            PP_100_DTHRHD,
            PP_99,
            PP_99_HR,
            PP_99_HD,
            PP_99_DT,
            PP_99_DTHD,
            PP_99_DTHR,
            PP_99_HRHD,
            PP_99_DTHRHD,
            PP_98,
            PP_98_HR,
            PP_98_HD,
            PP_98_DT,
            PP_98_DTHD,
            PP_98_DTHR,
            PP_98_HRHD,
            PP_98_DTHRHD,
            PP_97,
            PP_97_HR,
            PP_97_HD,
            PP_97_DT,
            PP_97_DTHD,
            PP_97_DTHR,
            PP_97_HRHD,
            PP_97_DTHRHD,
            beatmap_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, data)
        except:
            pass

        connexion.commit()
        connexion.close()

        return

    def print_beatmap(self):
        """Clean output to see this user parameters"""

        if self.beatmap_id == None:
            print('Beatmap empty')
            return

        print("---- Global informations ----")
        print("|")
        print("|-uso_id             = {}".format(self.uso_id))
        print("|-beatmapset_id      = {}".format(self.beatmapset_id))
        print("|-bpm                = {}".format(self.bpm))
        print("|-difficultyrating   = {}".format(self.difficultyrating))
        print("|-aim_stars          = {}".format(self.aim_stars))
        print("|-speed_stars        = {}".format(self.speed_stars))
        print("|-playstyle          = {}".format(self.playstyle))
        print("|-diff_size          = {}".format(self.diff_size))
        print("|-diff_overall       = {}".format(self.diff_overall))
        print("|-diff_approach      = {}".format(self.diff_approach))
        print("|-diff_drain         = {}".format(self.diff_drain))
        print("|-hit_length         = {}".format(self.hit_length))
        print("|-total_length       = {}".format(self.total_length))
        print("|-max_combo          = {}".format(self.max_combo))
        print("|-artist             = {}".format(self.artist))
        print("|-creator            = {}".format(self.creator))
        print("|-title              = {}".format(self.title))
        print("|-version            = {}".format(self.version))
        print("|-mode               = {}".format(self.mode))
        print("|-tags               = {}".format(self.tags))
        print("|-approved           = {}".format(self.approved))
        print("|-approved_date      = {}".format(self.approved_date))
        print("|-last_update        = {}".format(self.last_update))
        print("|")
        print("---- PP stats 100 ----")
        print("|")
        print("|-PP_100             = {}".format(self.PP_100))
        print("|-PP_100_HR          = {}".format(self.PP_100_HR))
        print("|-PP_100_HD          = {}".format(self.PP_100_HD))
        print("|-PP_100_DT          = {}".format(self.PP_100_DT))
        print("|-PP_100_DTHD        = {}".format(self.PP_100_DTHD))
        print("|-PP_100_DTHR        = {}".format(self.PP_100_DTHR))
        print("|-PP_100_HRHD        = {}".format(self.PP_100_HRHD))
        print("|-PP_100_DTHRHD      = {}".format(self.PP_100_DTHRHD))
        print("|")
        print("---- PP stats 99  ----")
        print("|")
        print("|-PP_99              = {}".format(self.PP_99))
        print("|-PP_99_HR           = {}".format(self.PP_99_HR))
        print("|-PP_99_HD           = {}".format(self.PP_99_HD))
        print("|-PP_99_DT           = {}".format(self.PP_99_DT))
        print("|-PP_99_DTHD         = {}".format(self.PP_99_DTHD))
        print("|-PP_99_DTHR         = {}".format(self.PP_99_DTHR))
        print("|-PP_99_HRHD         = {}".format(self.PP_99_HRHD))
        print("|-PP_99_DTHRHD       = {}".format(self.PP_99_DTHRHD))
        print("|")
        print("---- PP stats 98  ----")
        print("|")
        print("|-PP_98              = {}".format(self.PP_98))
        print("|-PP_98_HR           = {}".format(self.PP_98_HR))
        print("|-PP_98_HD           = {}".format(self.PP_98_HD))
        print("|-PP_98_DT           = {}".format(self.PP_98_DT))
        print("|-PP_98_DTHD         = {}".format(self.PP_98_DTHD))
        print("|-PP_98_DTHR         = {}".format(self.PP_98_DTHR))
        print("|-PP_98_HRHD         = {}".format(self.PP_98_HRHD))
        print("|-PP_98_DTHRHD       = {}".format(self.PP_98_DTHRHD))
        print("|")
        print("---- PP stats 97  ----")
        print("|")
        print("|-PP_97              = {}".format(self.PP_97))
        print("|-PP_97_HR           = {}".format(self.PP_97_HR))
        print("|-PP_97_HD           = {}".format(self.PP_97_HD))
        print("|-PP_97_DT           = {}".format(self.PP_97_DT))
        print("|-PP_97_DTHD         = {}".format(self.PP_97_DTHD))
        print("|-PP_97_DTHR         = {}".format(self.PP_97_DTHR))
        print("|-PP_97_HRHD         = {}".format(self.PP_97_HRHD))
        print("|-PP_97_DTHRHD       = {}".format(self.PP_97_DTHRHD))
        print("|")

        return

    def use_pyttanko(self, beatmap):
        """Processing beatmap to extrace juicy pp stats"""

        hr = pyttanko.MODS_HR
        hd = pyttanko.MODS_HD
        dt = pyttanko.MODS_DT

        mods = [0, hd, hr, dt, hd|dt, hd|hr, dt|hr, hd|dt|hr]
        accs = [97, 98, 99, 100]

        peppers = {}

        #This is where the magic happends, woahhhh *.*
        for mod in mods:
            for acc in accs:

                n300, n100, n50 = pyttanko.acc_round(acc, len(beatmap.hitobjects), 0)
                stars = pyttanko.diff_calc().calc(beatmap, mods=mod)
                pp, _, _, _, _ = pyttanko.ppv2(stars.aim, stars.speed,
                    bmap=beatmap, mods=mod, n300=n300, n100=n100, n50=n50, nmiss=0)
                peppers[pyttanko.mods_str(mod), str(acc)] = (pp, stars)

        return peppers

    def in_database(self):
        """ Checks if the beatmaps is in the database"""
        return self.uso_id != 0

    def beatmap_string(self):
        """Returns the beatmap_str or import it if needed"""

        if self.beatmaps_str != "":
            return self.beatmaps_str

        if self.beatmap_id == 0:
            return ""

        if (not self.session):
            r = requests.get('https://osu.ppy.sh/osu/{}'.format(self.beatmap_id))
        else:
            r = self.session.get('https://osu.ppy.sh/osu/{}'.format(self.beatmap_id))

        self.beatmaps_str = r.text

        return self.beatmaps_str

    def import_beatmap(self):
        """ Imports a beatmap into the database """

        #Checking ig the beatmap is already imported
        if self.in_database():
            return 0

        print('Importing beatmap {}'.format(self.beatmap_id))

        beatmap = pyttanko.parser().map(io.StringIO(self.beatmap_string()))
        peppers = self.use_pyttanko(beatmap)

        if (round(peppers['nomod', '100'][1].total, 2) == 0):
            return 0

        #The beatmap seems to be fine, fetching api datas
        api_data = get_beatmap(self.settings['osu_api_key'], self.beatmap_id, self.session)
        if (api_data[0]):
            api_data = api_data[0]
        else:
            return 0

        self.difficultyrating   = round(peppers['nomod', '100'][1].total, 2)
        self.aim_stars          = round(peppers['nomod', '100'][1].aim,   2)
        self.speed_stars        = round(peppers['nomod', '100'][1].speed, 2)

        self.playstyle          = self.speed_stars / self.difficultyrating

        self.diff_size          = beatmap.cs
        self.diff_overall       = beatmap.od
        self.diff_approach      = beatmap.ar
        self.diff_drain         = beatmap.hp

        self.beatmapset_id      = int  (api_data['beatmapset_id'])
        self.total_length       = int  (api_data['total_length'])
        self.hit_length         = int  (api_data['hit_length'])
        self.bpm                = float(api_data['bpm'])
        self.approved_date      = api_data['approved_date']
        self.last_update        = api_data['last_update']
        self.approved           = api_data['approved']
        self.tags               = api_data['tags']

        self.max_combo          = beatmap.max_combo()
        self.artist             = beatmap.artist
        self.creator            = beatmap.creator
        self.title              = beatmap.title
        self.version            = beatmap.version
        self.mode               = beatmap.mode

        self.PP_100             = round(peppers['nomod', '100'][0])
        self.PP_100_HR          = round(peppers['HR',    '100'][0])
        self.PP_100_HD          = round(peppers['HD',    '100'][0])
        self.PP_100_DT          = round(peppers['DT',    '100'][0])
        self.PP_100_DTHD        = round(peppers['HDDT',  '100'][0])
        self.PP_100_DTHR        = round(peppers['HRDT',  '100'][0])
        self.PP_100_HRHD        = round(peppers['HDHR',  '100'][0])
        self.PP_100_DTHRHD      = round(peppers['HDHRDT','100'][0])

        self.PP_99              = round(peppers['nomod', '99'][0])
        self.PP_99_HR           = round(peppers['HR',    '99'][0])
        self.PP_99_HD           = round(peppers['HD',    '99'][0])
        self.PP_99_DT           = round(peppers['DT',    '99'][0])
        self.PP_99_DTHD         = round(peppers['HDDT',  '99'][0])
        self.PP_99_DTHR         = round(peppers['HRDT',  '99'][0])
        self.PP_99_HRHD         = round(peppers['HDHR',  '99'][0])
        self.PP_99_DTHRHD       = round(peppers['HDHRDT','99'][0])

        self.PP_98              = round(peppers['nomod', '98'][0])
        self.PP_98_HR           = round(peppers['HR',    '98'][0])
        self.PP_98_HD           = round(peppers['HD',    '98'][0])
        self.PP_98_DT           = round(peppers['DT',    '98'][0])
        self.PP_98_DTHD         = round(peppers['HDDT',  '98'][0])
        self.PP_98_DTHR         = round(peppers['HRDT',  '98'][0])
        self.PP_98_HRHD         = round(peppers['HDHR',  '98'][0])
        self.PP_98_DTHRHD       = round(peppers['HDHRDT','98'][0])

        self.PP_97              = round(peppers['nomod', '97'][0])
        self.PP_97_HR           = round(peppers['HR',    '97'][0])
        self.PP_97_HD           = round(peppers['HD',    '97'][0])
        self.PP_97_DT           = round(peppers['DT',    '97'][0])
        self.PP_97_DTHD         = round(peppers['HDDT',  '97'][0])
        self.PP_97_DTHR         = round(peppers['HRDT',  '97'][0])
        self.PP_97_HRHD         = round(peppers['HDHR',  '97'][0])
        self.PP_97_DTHRHD       = round(peppers['HDHRDT','97'][0])

        return 1


if __name__ == '__main__':

    file = open('beatmaps.txt', 'r')
    lines = file.readlines()

    for line in lines:
        id = int(line.strip('https://osu.ppy.sh/b/'))
        beatmap = Beatmap(id)