# -*- coding: utf-8 -*-

"""
    Osu users library for uso bot
    By Renondedju and Jamu
"""

import os
import sys
import json
import time
import sqlite3
import asyncio

sys.path.append(os.path.realpath('../'))

from libs.osuapi  import get_user, get_user_best
from libs.beatmap import Beatmap
from libs.mods    import Mode, Mods
from libs         import pyttanko

class User():
    """ User informations """

    def __init__(self, osu_id:int = 0, osu_name:str = "", discord_id:int = 0):
        """ Init """

        self.settings      = json.loads(open('../config.json', 'r').read())
        self.database_path = self.settings['database_path']

        #Logs infos
        self.discord_name = "None"
        self.discord_icon = "None"

        #Global informations
        self.osu_id     = osu_id
        self.uso_id     = 0
        self.discord_id = discord_id
        self.osu_name   = osu_name
        self.rank       = 0
        self.raw_pp     = 0

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
        self.playrate_dict      = {}
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
        self.last_update             = 0 #timestamp

        self.load_user_profile()

    def set_logs_infos(self, discord_name:str, discord_icon:str, discord_id:int):
        """ Seting discord_name and discord_icon"""
        self.discord_icon = discord_icon
        self.discord_name = discord_name
        self.discord_id   = discord_id

    def load_user_profile(self):
        """ Loading a user profile from the database """
        if (self.osu_id     == 0  and
            self.osu_name   == "" and
            self.discord_id == 0) or not self.database_path:
            return

        #Connecting to database
        connexion = sqlite3.connect(self.database_path)
        cursor = connexion.cursor()
        
        #Fetching datas from database
        if self.osu_id != 0:
            query = cursor.execute("SELECT * FROM users WHERE osu_id     = ?", [self.osu_id,])
        elif self.osu_name != "":
            query = cursor.execute("SELECT * FROM users WHERE osu_name   = ?", [self.osu_name,])
        elif self.discord_id != 0:
            query = cursor.execute("SELECT * FROM users WHERE discord_id = ?", [self.discord_id,])

        #Making a cool looking dictionary
        colname = [ d[0] for d in query.description ]
        result_list = [ dict(zip(colname, r)) for r in query]

        if len(result_list) == 0:
            connexion.close()

            #No coresponding user, so importing it
            print ('Importing user id {}'.format(self.osu_id))
            self.update_user_stats()
            self.save_user_profile()

            return
        
        self.uso_id     = result_list[0]['uso_id']
        self.discord_id = result_list[0]['discord_id']
        self.osu_id     = result_list[0]['osu_id']
        self.osu_name   = result_list[0]['osu_name']
        self.rank       = result_list[0]['rank']
        self.raw_pp     = result_list[0]['raw_pp']
        
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
        self.last_update                = result_list[0]['last_update'] #timestamp
        
        connexion.close()

        self.update_user_stats()

        return

    def is_empty(self):
        """ Checks if a user has been loaded or imported """
        return self.osu_id == 0 and self.osu_name == ""

    def save_user_profile(self):
        """ Saves the user profile into a given database """
        if (self.osu_id == 0 and self.osu_name == "") or not self.database_path:
            return

        data = [self.discord_id,
            self.osu_name,
            self.rank,
            self.raw_pp,
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
            self.DT_recommended,
            self.DTHD_recommended,
            self.DTHR_recommended, 
            self.HRHD_recommended,
            self.DTHRHD_recommended,
            self.playstyle,
            self.api_key,
            self.request_rate,
            self.requests_max,
            self.donations,
            self.last_discord_patch_used,
            self.last_irc_patch_used,
            self.last_update,
            self.osu_id,]

        connexion = sqlite3.connect(self.database_path)
        cursor = connexion.cursor()

        if self.osu_id != 0:
            cursor.execute("SELECT * FROM users WHERE osu_id = ?", [self.osu_id,])
        else:
            cursor.execute("SELECT * FROM users WHERE osu_name = ?", [self.osu_name,])

        #Checking if the user already exists in the database
        if not cursor.fetchall():
            #if not, creating a new row
            cursor.execute("""INSERT INTO users 
            (discord_id,
            osu_name,
            rank,
            raw_pp,
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
            DT_recommended,
            DTHD_recommended,
            DTHR_recommended,
            HRHD_recommended,
            DTHRHD_recommended,
            playstyle,
            api_key,
            request_rate,
            requests_max,
            donations,
            last_discord_patch_used,
            last_irc_patch_used,
            last_update,
            osu_id)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, 
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
            ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, data)
        else:
            #otherwise updating it
            cursor.execute("""UPDATE users SET
                discord_id              = ?,
                osu_name                = ?,
                rank                    = ?,
                raw_pp                  = ?,
                accuracy_average        = ?,
                pp_average              = ?,
                bpm_low                 = ?,
                bpm_average             = ?,
                bpm_high                = ?,
                od_average              = ?,
                ar_average              = ?,
                cs_average              = ?,
                len_average             = ?,
                Nomod_playrate          = ?,
                HR_playrate             = ?,
                HD_playrate             = ?,
                DT_playrate             = ?,
                DTHD_playrate           = ?,
                DTHR_playrate           = ?,
                HRHD_playrate           = ?,
                DTHRHD_playrate         = ?,
                Nomod_recommended       = ?,
                HR_recommended          = ?,
                HD_recommended          = ?,
                DT_recommended          = ?,
                DTHD_recommended        = ?,
                DTHR_recommended        = ?,
                HRHD_recommended        = ?,
                DTHRHD_recommended      = ?,
                playstyle               = ?,
                api_key                 = ?,
                request_rate            = ?,
                requests_max            = ?,
                donations               = ?,
                last_discord_patch_used = ?,
                last_irc_patch_used     = ?,
                last_update             = ?,
                osu_id                  = ?
                WHERE uso_id = {}
            """.format(self.uso_id), data)

        connexion.commit()
        connexion.close()

        return

    def reset_recommendations(self):
        """ Reseting all recommendations to 0 """

        self.Nomod_recommended  = ""
        self.HR_recommended     = ""
        self.HD_recommended     = ""
        self.DT_recommended     = ""
        self.DTHD_recommended   = ""
        self.DTHR_recommended   = ""
        self.HRHD_recommended   = ""
        self.DTHRHD_recommended = ""

        print ('Recommendations for {} reseted !'.format(self.osu_name))

        self.save_user_profile()

        return

    def get_recommended(self, mods:str, recommended:str = ''):
        """ Gives the already recommended maps for a specific mod """
        
        mods = mods.strip('_')

        if (recommended != ''):
            recommended = ', ' + recommended

        if (mods == 'HR'):
            if (self.HR_recommended == None):
                self.HR_recommended = ''
            self.HR_recommended += recommended
            return self.HR_recommended

        if (mods == 'HD'):
            if (self.HD_recommended == None):
                self.HD_recommended = ''
            self.HD_recommended += recommended
            return self.HD_recommended

        if (mods == 'DT'):
            if (self.DT_recommended == None):
                self.DT_recommended = ''
            self.DT_recommended += recommended
            return self.DT_recommended

        if (mods == 'DTHD'):
            if (self.DTHD_recommended == None):
                self.DTHD_recommended = ''
            self.DTHD_recommended += recommended
            return self.DTHD_recommended

        if (mods == 'DTHR'):
            if (self.DTHR_recommended == None):
                self.DTHR_recommended = ''
            self.DTHR_recommended += recommended
            return self.DTHR_recommended

        if (mods == 'HRHD'):
            if (self.HRHD_recommended == None):
                self.HRHD_recommended = ''
            self.HRHD_recommended += recommended
            return self.HRHD_recommended

        if (mods == 'DTHRHD'):
            if (self.DTHRHD_recommended == None):
                self.DTHRHD_recommended = ''
            self.DTHRHD_recommended += recommended
            return self.DTHRHD_recommended

        if (self.Nomod_recommended == None):
                self.Nomod_recommended = ''
        self.Nomod_recommended += recommended
        return self.Nomod_recommended

    def update_user_stats(self, force_update:bool = False):
        """ Updating user stats """

        if self.osu_id == 0 and self.osu_name == "":
            return

        #Time to update :D
        #Updating only if one day has passed
        if self.last_update > time.time() - 86400 and not force_update: #86400 is the number of secs in one day
            return

        print ("Updating {}, {} users stats".format(self.osu_id, self.osu_name))

        #Fetching datas from bancho api
        if self.osu_id != 0:
            userinfo = get_user(self.settings['osu_api_key'], self.osu_id, Mode.Osu)
        elif self.osu_name != "":
            userinfo = get_user(self.settings['osu_api_key'], self.osu_name, Mode.Osu)

        if (len(userinfo) == 0):
            print('User id {}, {} does not exists !'.format(self.osu_id, self.osu_name))
            return
        else:
            userinfo = userinfo[0]

        #Well, you might not have won enougth pp for now 
        if (abs(self.raw_pp - float(userinfo['pp_raw']))) < 1.5 and not force_update:
            return

        self.osu_id             = userinfo['user_id']
        self.osu_name           = userinfo['username']
        self.rank               = int(userinfo['pp_rank'])
        self.raw_pp             = float(userinfo['pp_raw'])

        if self.osu_id != 0:
            userbest = get_user_best(self.settings['osu_api_key'], self.osu_id, Mode.Osu, 20)
        elif self.osu_name != "":
            userbest = get_user_best(self.settings['osu_api_key'], self.osu_name, Mode.Osu, 20)

        self.playstyle          = 0
        self.accuracy_average   = 0
        self.cs_average         = 0
        self.ar_average         = 0
        self.od_average         = 0
        self.pp_average         = 0
        self.len_average        = 0
        self.bpm_average        = []

        self.playrate_dict   = {}
        self.Nomod_playrate  = 0.0
        self.HR_playrate     = 0.0
        self.HD_playrate     = 0.0
        self.DT_playrate     = 0.0
        self.DTHD_playrate   = 0.0
        self.DTHR_playrate   = 0.0
        self.HRHD_playrate   = 0.0
        self.DTHRHD_playrate = 0.0

        #Main loop
        for score in userbest:
            
            beatmap = Beatmap(int(score['beatmap_id']))
            
            self.accuracy_average   += pyttanko.acc_calc(int(score['count300']), int(score['count100']), int(score['count50']), int(score['countmiss']))
            self.pp_average         += float(score['pp'])
            self.cs_average         += beatmap.diff_size
            self.ar_average         += beatmap.diff_approach
            self.od_average         += beatmap.diff_overall
            self.len_average        += int(beatmap.hit_length)

            self.bpm_average.append(beatmap.bpm)
            self.playstyle   += beatmap.playstyle

            #Mods playrate

            mod = pyttanko.mods_str(int(score['enabled_mods']))
            if not mod in self.playrate_dict:
                self.playrate_dict[mod] = 100.0 / 20.0
            else:
                self.playrate_dict[mod] += 100.0 / 20.0

        if 'nomod' in self.playrate_dict:   #None
            self.Nomod_playrate   = self.playrate_dict['nomod']
        if 'HR' in self.playrate_dict:      #HR
            self.HR_playrate      = self.playrate_dict['HR']
        if 'HD' in self.playrate_dict:      #HD
            self.HD_playrate      = self.playrate_dict['HD']
        if 'DT' in self.playrate_dict:      #DT
            self.DT_playrate      = self.playrate_dict['DT']
        if 'HDDT' in self.playrate_dict:    #HDDT
            self.DTHD_playrate    = self.playrate_dict['HDDT']
        if 'HRDT' in self.playrate_dict:    #HRDT
            self.DTHR_playrate    = self.playrate_dict['HRDT']
        if 'HDHR' in self.playrate_dict:    #HDHR
            self.HRHD_playrate    = self.playrate_dict['HDHR']
        if 'HDHRDT' in self.playrate_dict:  #HDHRDT
            self.DTHRHD_playrate  = self.playrate_dict['HDHRDT']
        # Nightcore should be considered Double Time to uso
        if 'NC' in self.playrate_dict:      #NC
            self.DT_playrate     += self.playrate_dict['NC']
        if 'HDNC' in self.playrate_dict:    #HDNC
            self.DTHD_playrate   += self.playrate_dict['HDNC']
        if 'HDHRNC' in self.playrate_dict:  #HDHRNC
            self.DTHRHD_playrate += self.playrate_dict['HDHRNC']

        self.playstyle          /= 20.0
        self.pp_average         = round(self.pp_average  / 20.0)
        self.cs_average         = round(self.cs_average  / 20.0)
        self.ar_average         = round(self.ar_average  / 20.0)
        self.od_average         = round(self.od_average  / 20.0)
        self.len_average        = round(self.len_average / 20.0)
        self.accuracy_average   = round(self.accuracy_average / 0.2)
        self.bpm_high           = round(max(self.bpm_average))
        self.bpm_low            = round(min(self.bpm_average))
        self.bpm_average        = round(sum(self.bpm_average) / len(self.bpm_average))

        self.last_update = time.time()

        self.save_user_profile()
    
        return

    def get_pyttanko(self, bmap, mods:int, n300:int, n100:int, n50:int, nmiss:int, combo:int):
        """ PP calculation function """

        stars = pyttanko.diff_calc().calc(bmap, mods=mods)
        pp, _, _, _, _ = pyttanko.ppv2(stars.aim, stars.speed, bmap=bmap, mods=int(mods), n300=int(n300), n100=int(n100), n50=int(n50), nmiss=int(nmiss), combo=int(combo))
        
        return (pp, stars)

    def print_user_profile(self):
        """Clean output to see this user parameters"""

        if self.osu_id == 0 and self.osu_name == "":
            print('User empty')
            return

        print("---- Global informations ----")
        print("|")
        print("|-osu_id      = {}".format(self.osu_id))
        print("|-uso_id      = {}".format(self.uso_id))
        print("|-discord_id  = {}".format(self.discord_id))
        print("|-osu_name    = {}".format(self.osu_name))
        print("|-rank        = {}".format(self.rank))
        print("|-raw_pp      = {}".format(self.raw_pp))
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
        print("|-last_update                = {}".format(self.last_update))
        print("|")


        return

if __name__ == '__main__':
    # --- Test lines !
    user = User(osu_name = "filsdelama")
    user.print_user_profile()