# -*- coding: utf-8 -*-
import pyttanko
import sqlite3
import asyncio
import json
import os, sys
sys.path.append(os.path.realpath('../'))

from libs.osuapi  import get_user, get_user_best
from libs.beatmap import Beatmap
from libs.mods    import Mode, Mods

class User():
    """ User informations """

    def __init__(self, osu_id:int):
        
        self.settings = json.loads(open('../config.json', 'r').read())
        self.database_path = self.settings['database_path']

        #Logs infos
        self.discord_name = "None"
        self.discord_icon = "None"

        #Global informations
        self.osu_id     = osu_id
        self.uso_id     = 0
        self.discord_id = 0
        self.osu_name   = 0
        self.rank       = 0

        #User performances
        self.accuracy_average   = 0
        self.pp_average         = 0
        self.bpm_low            = 0
        self.bpm_average        = 0
        self.bpm_high           = 0
        self.od_average         = 0
        self.ar_average         = 0
        self.cs_average         = 0
        self.len_average        = 0 #Drain

        #Mods playrate
        self.Nomod_playrate     = 0
        self.HR_playrate        = 0
        self.HD_playrate        = 0
        self.DT_playrate        = 0
        self.DTHD_playrate      = 0
        self.DTHR_playrate      = 0
        self.HRHD_playrate      = 0
        self.DTHRHD_playrate    = 0

        #Mods recommended
        self.Nomod_recommended  = ""
        self.HR_recommended     = ""
        self.HD_recommended     = ""
        self.DT_recommended     = ""
        self.DTHD_recommended   = ""
        self.DTHR_recommended   = ""
        self.HRHD_recommended   = ""
        self.DTHRHD_recommended = ""

        #Playstyle -> Jumps 0 -----|----- 1 Stream
        self.playstyle    = 0.5

        #Api settings
        self.api_key      = "None"
        self.request_rate = 0 # Requests/min (beatmaps requests)

        #Money bonuses
        self.requests_max = 5
        self.donations    = 0

        #Patch
        self.last_discord_patch_used = "0.0.0"
        self.last_irc_patch_used     = "0.0.0"
        self.last_time_played        = 0 #timestamp

        self.load_user_profile()

    def set_logs_infos(self, discord_name:str, discord_icon:str):
        """ Seting discord_name and discord_icon"""
        self.discord_icon = discord_icon
        self.discord_name = discord_name

    def load_user_profile(self):
        """ Loading a user profile from the database """
        if not self.osu_id or not self.database_path:
            return

        connexion = sqlite3.connect(self.database_path)
        cursor = connexion.cursor()
        
        query = cursor.execute("SELECT * FROM users WHERE osu_id = ?", [self.osu_id,])
        
        #Making a cool looking dictionary
        colname = [ d[0] for d in query.description ]
        result_list = [ dict(zip(colname, r)) for r in query]
        
        if len(result_list) == 0:
            connexion.close()

            #No coresponding user, so importing it
            self.update_user_stats()
            self.save_user_profile()

            return
        
        self.uso_id     = result_list[0]['uso_id']
        self.discord_id = result_list[0]['discord_id']
        self.osu_name   = result_list[0]['osu_name']
        self.rank       = result_list[0]['rank']
        
        #User performances
        self.accuracy_average   = result_list[0]['accuracy_average']
        self.pp_average         = result_list[0]['pp_average']
        self.bpm_low            = result_list[0]['bpm_low']
        self.bpm_average        = result_list[0]['bpm_average']
        self.bpm_high           = result_list[0]['bpm_high']
        self.od_average         = result_list[0]['od_average']
        self.ar_average         = result_list[0]['ar_average']
        self.cs_average         = result_list[0]['cs_average']
        self.len_average        = result_list[0]['len_average'] #Drain
        
        #Mods playrate
        self.Nomod_playrate     = result_list[0]['Nomod_playrate']
        self.HR_playrate        = result_list[0]['HR_playrate']
        self.HD_playrate        = result_list[0]['HD_playrate']
        self.DT_playrate        = result_list[0]['DT_playrate']
        self.DTHD_playrate      = result_list[0]['DTHD_playrate']
        self.DTHR_playrate      = result_list[0]['DTHR_playrate']
        self.HRHD_playrate      = result_list[0]['HRHD_playrate']
        self.DTHRHD_playrate    = result_list[0]['DTHRHD_playrate']
        
        #Mods recommended
        self.Nomod_recommended  = result_list[0]['Nomod_recommended']
        self.HR_recommended     = result_list[0]['HR_recommended']
        self.HD_recommended     = result_list[0]['HD_recommended']
        self.DT_recommended     = result_list[0]['DT_recommended']
        self.DTHD_recommended   = result_list[0]['DTHD_recommended']
        self.DTHR_recommended   = result_list[0]['DTHR_recommended']
        self.HRHD_recommended   = result_list[0]['HRHD_recommended']
        self.DTHRHD_recommended = result_list[0]['DTHRHD_recommended']
        
        #Playstyle -> Jumps 0 -----|----- 1 Stream
        self.playstyle = result_list[0]['playstyle']
        
        #Api settings
        self.api_key        = result_list[0]['api_key']
        self.request_rate   = result_list[0]['request_rate'] # Requests/min (beatmaps requests)
        
        #Money bonuses
        self.requests_max   = result_list[0]['requests_max']
        self.donations      = result_list[0]['donations']
        
        #Patch
        self.last_discord_patch_used    = result_list[0]['last_discord_patch_used']
        self.last_irc_patch_used        = result_list[0]['last_irc_patch_used']
        self.last_time_played           = result_list[0]['last_time_played'] #timestamp
        
        connexion.close()

        return

    def save_user_profile(self):
        """ Saves the user profile into a given database """
        if not self.osu_id or not self.database_path:
            return

        connexion = sqlite3.connect(self.database_path)
        cursor = connexion.cursor()

        data = [self.discord_id,
            self.osu_name,
            self.rank,
            self.accuracy_average,
            self.pp_average,
            self.bpm_low,
            self.bpm_average,
            self.bpm_high,
            self.od_average,
            self.ar_average,
            self.cs_average,
            self.len_average,
            self.Nomod_playrate,
            self.HR_playrate,
            self.HD_playrate,
            self.DT_playrate,
            self.DTHD_playrate,
            self.DTHR_playrate,
            self.HRHD_playrate,
            self.DTHRHD_playrate,
            self.Nomod_recommended,
            self.HR_recommended,
            self.HD_recommended,
            self.DTHR_recommended,
            self.DTHD_recommended,
            self.DTHR_recommended, 
            self.HRHD_recommended,
            self.playstyle,
            self.api_key,
            self.request_rate,
            self.requests_max,
            self.donations,
            self.last_discord_patch_used,
            self.last_irc_patch_used,
            self.last_time_played,
            self.osu_id,]

        try:
            cursor.execute(""" INSERT OR REPLACE INTO users
            (discord_id,
            osu_name,
            rank,
            accuracy_average,
            pp_average,
            bpm_low,
            bpm_average,
            bpm_high,
            od_average,
            ar_average,
            cs_average,
            len_average,
            Nomod_playrate,
            HR_playrate,
            HD_playrate,
            DT_playrate,
            DTHD_playrate,
            DTHR_playrate,
            HRHD_playrate,
            DTHRHD_playrate,
            Nomod_recommended,
            HR_recommended,
            HD_recommended,
            DTHR_recommended,
            DTHD_recommended,
            DTHR_recommended, 
            HRHD_recommended,
            playstyle,
            api_key,
            request_rate,
            requests_max,
            donations,
            last_discord_patch_used,
            last_irc_patch_used,
            last_time_played,
            osu_id)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, data)
        except Exception as e:
            print('\033[91mFailed to save user (id = {}, name = {})\n{}: {}\033[0m'.format(self.osu_id, self.osu_name, type(e).__name__, e))
            connexion.close()
            return

        connexion.commit()
        connexion.close()

        return

    def update_user_stats(self):
        """ Updating user stats """

        if not self.osu_id:
            return

        print ("Updating {}, {} users stats".format(self.osu_id, self.osu_name))

        userinfo = get_user(self.settings['osu_api_key'], self.osu_id, Mode.Osu)[0]
        userbest = get_user_best(self.settings['osu_api_key'], self.osu_id, Mode.Osu, 20)

        # print (userbest)

        self.osu_name           = userinfo['username']
        self.rank               = int(userinfo['pp_rank'])
        self.playstyle          = 0
        self.accuracy_average   = 0
        self.cs_average         = 0
        self.ar_average         = 0
        self.od_average         = 0
        self.pp_average         = 0
        self.bpm_average        = []

        for score in userbest:
            
            beatmap = Beatmap(int(score['beatmap_id']))
            if (beatmap.import_beatmap()):
                beatmap.save_beatmap()

            btmap       = pyttanko.parser().map(open("{}/{}.osu".format(beatmap.beatmaps_path, beatmap.beatmap_id)))
            pp, stars   = self.get_pyttanko(btmap, int(score['enabled_mods']), score['count300'], score['count100'], score['count50'], score['countmiss'], score['maxcombo'])
            
            self.accuracy_average   += pyttanko.acc_calc(int(score['count300']), int(score['count100']), int(score['count50']), int(score['countmiss']))
            self.pp_average         += float(score['pp'])
            self.cs_average         += btmap.cs
            self.ar_average         += btmap.ar
            self.od_average         += btmap.od

            self.bpm_average.append(beatmap.get_bpm(btmap))
            self.playstyle   += stars.speed / stars.total

            #Mods playrate

            if (score['enabled_mods'] == '0'):   #None
                self.Nomod_playrate  += 100.0 / 20.0;
            if (score['enabled_mods'] == '16'):  #HR
                self.HR_playrate     += 100.0 / 20.0;
            if (score['enabled_mods'] == '8'):   #HD
                self.HD_playrate     += 100.0 / 20.0;
            if (score['enabled_mods'] == '64'):  #DT
                self.DT_playrate     += 100.0 / 20.0;
            if (score['enabled_mods'] == '72'):  #DTHD
                self.DTHD_playrate   += 100.0 / 20.0;
            if (score['enabled_mods'] == '80'):  #DTHR
                self.DTHR_playrate   += 100.0 / 20.0;
            if (score['enabled_mods'] == '24'):  #HRHD
                self.HRHD_playrate   += 100.0 / 20.0;
            if (score['enabled_mods'] == '88'):  #DTHDHR
                self.DTHRHD_playrate += 100.0 / 20.0;

        self.playstyle          /= 20.0
        self.pp_average         = round(self.pp_average / 20.0)
        self.cs_average         = round(self.cs_average / 20.0)
        self.ar_average         = round(self.ar_average / 20.0)
        self.od_average         = round(self.od_average / 20.0)
        self.accuracy_average   = round(self.accuracy_average / 0.2)
        self.bpm_high           = round(max(self.bpm_average))
        self.bpm_low            = round(min(self.bpm_average))
        self.bpm_average        = round(sum(self.bpm_average) / len(self.bpm_average))
    
        return

    def get_pyttanko(self, bmap, mods:int, n300:int, n100:int, n50:int, nmiss:int, combo:int):
        stars = pyttanko.diff_calc().calc(bmap, mods=mods)
        pp, _, _, _, _ = pyttanko.ppv2(stars.aim, stars.speed, bmap=bmap, mods=int(mods), n300=int(n300), n100=int(n100), n50=int(n50), nmiss=int(nmiss), combo=int(combo))
        return (pp, stars)

    def print_user_profile(self):
        """Clean output to see this user parameters"""

        if self.uso_id == None:
            print('User empty')
            return

        print("---- Global informations ----")
        print("|")
        print("|-osu_id      = {}".format(self.osu_id))
        print("|-uso_id      = {}".format(self.uso_id))
        print("|-discord_id  = {}".format(self.discord_id))
        print("|-osu_name    = {}".format(self.osu_name))
        print("|-rank        = {}".format(self.rank))
        print("|")
        print("---- User performances ----")
        print("|")
        print("|-accuracy_average   = {}".format(self.accuracy_average))
        print("|-pp_average         = {}".format(self.pp_average))
        print("|-bpm_low            = {}".format(self.bpm_low))
        print("|-bpm_average        = {}".format(self.bpm_average))
        print("|-bpm_high           = {}".format(self.bpm_high))
        print("|-od_average         = {}".format(self.od_average))
        print("|-ar_average         = {}".format(self.ar_average))
        print("|-cs_average         = {}".format(self.cs_average))
        print("|-len_average        = {}".format(self.len_average))
        print("|")
        print("---- Mods playrate ----")
        print("|")
        print("|-Nomod      = {}%".format(self.Nomod_playrate))
        print("|-HR         = {}%".format(self.HR_playrate))
        print("|-HD         = {}%".format(self.HD_playrate))
        print("|-DT         = {}%".format(self.DT_playrate))
        print("|-DTHD       = {}%".format(self.DTHD_playrate))
        print("|-DTHR       = {}%".format(self.DTHR_playrate))
        print("|-HRHD       = {}%".format(self.HRHD_playrate))
        print("|-DTHRHD     = {}%".format(self.DTHRHD_playrate))
        print("|")
        print("---- Playstyle ----")
        print("|")
        print("|-playstyle  = {}".format(self.playstyle))
        print("|")
        print("---- Api settings ----")
        print("|")
        print("|-api_key        = {}".format(self.api_key))
        print("|-request_rate   = {} requests/min".format(self.request_rate))
        print("|")
        print("---- Money bonuses ----")
        print("|")
        print("|-requests_max   = {} beatmaps/request".format(self.requests_max))
        print("|-donations      = {}€".format(self.donations))
        print("|")
        print("---- Patch ----")
        print("|")
        print("|-last_discord_patch_used    = {}".format(self.last_discord_patch_used))
        print("|-last_irc_patch_used        = {}".format(self.last_irc_patch_used))
        print("|-last_time_played           = {}".format(self.last_time_played))
        print("|")


        return

if __name__ == '__main__':
    # --- Test lines !
    user = User(7418575)
    user.update_user_stats()
    user.save_user_profile()
    user.print_user_profile()