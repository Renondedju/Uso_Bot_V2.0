# -*- coding: utf-8 -*-
import sqlite3, json
from osuapi import get_user, get_user_best
import pyttanko

class User():
	""" User informations """

	def __init__(self, osu_id, database_path):
		
		#Logs infos
		self.discord_name = None
		self.discord_icon = None

		#Global informations
		self.osu_id = osu_id
		self.uso_id = None
		self.discord_id = None
		self.osu_name = None
		self.rank = None

		#User performances
		self.accuracy_average = None
		self.pp_average = None
		self.bpm_low = None
		self.bpm_average = None
		self.bpm_high = None
		self.od_average = None
		self.ar_average = None
		self.cs_average = None
		self.len_average = None #Drain

		#Mods playrate
		self.Nomod_playrate = None
		self.HR_playrate = None
		self.HD_playrate = None
		self.DT_playrate = None
		self.DTHD_playrate = None
		self.DTHR_playrate = None
		self.HRHD_playrate = None
		self.DTHRHD_playrate = None

		#Mods recommended
		self.Nomod_recommended = None
		self.HR_recommended = None
		self.HD_recommended = None
		self.DT_recommended = None
		self.DTHD_recommended = None
		self.DTHR_recommended = None
		self.HRHD_recommended = None
		self.DTHRHD_recommended = None

		#Playstyle -> Jumps 0 -----|----- 1 Stream
		self.playstyle = None

		#Api settings
		self.api_key = None
		self.request_rate = 0 # Requests/min (beatmaps requests)

		#Money bonuses
		self.requests_max = 5
		self.donations = 0

		#Patch
		self.last_discord_patch_used = "0.0.0"
		self.last_irc_patch_used = "0.0.0"
		self.last_time_played = 0 #timestamp

		self.load_user_profile(database_path)

	def set_logs_infos(self, discord_name, discord_icon):
		""" Seting discord_name and discord_icon"""
		self.discord_icon = discord_icon
		self.discord_name = discord_name

	def load_user_profile(self, database_path):
		""" Loading a user profile from the database """
		if not self.osu_id or not database_path:
			return

		connexion = sqlite3.connect(database_path)
		cursor = connexion.cursor()
		
		query = cursor.execute("SELECT * FROM users WHERE osu_id = ?", [self.osu_id,])
		
		#Making a cool looking dictionary
		colname = [ d[0] for d in query.description ]
		result_list = [ dict(zip(colname, r)) for r in query.fetchall()]
		
		if len(result_list) == 0:
			connexion.close()
			return #No coresponding user
		
		self.uso_id 	= result_list[0]['uso_id']
		self.discord_id = result_list[0]['discord_id']
		self.osu_name 	= result_list[0]['osu_name']
		self.rank 		= result_list[0]['rank']
		
		#User performances
		self.accuracy_average 	= result_list[0]['accuracy_average']
		self.pp_average 		= result_list[0]['pp_average']
		self.bpm_low 			= result_list[0]['bpm_low']
		self.bpm_average 		= result_list[0]['bpm_average']
		self.bpm_high 			= result_list[0]['bpm_high']
		self.od_average 		= result_list[0]['od_average']
		self.ar_average 		= result_list[0]['ar_average']
		self.cs_average 		= result_list[0]['cs_average']
		self.len_average 		= result_list[0]['len_average'] #Drain
		
		#Mods playrate
		self.Nomod_playrate 	= result_list[0]['Nomod_playrate']
		self.HR_playrate 		= result_list[0]['HR_playrate']
		self.HD_playrate 		= result_list[0]['HD_playrate']
		self.DT_playrate 		= result_list[0]['DT_playrate']
		self.DTHD_playrate 		= result_list[0]['DTHD_playrate']
		self.DTHR_playrate 		= result_list[0]['DTHR_playrate']
		self.HRHD_playrate 		= result_list[0]['HRHD_playrate']
		self.DTHRHD_playrate 	= result_list[0]['DTHRHD_playrate']
		
		#Mods recommended
		self.Nomod_recommended 	= result_list[0]['Nomod_recommended']
		self.HR_recommended 	= result_list[0]['HR_recommended']
		self.HD_recommended 	= result_list[0]['HD_recommended']
		self.DT_recommended 	= result_list[0]['DT_recommended']
		self.DTHD_recommended 	= result_list[0]['DTHD_recommended']
		self.DTHR_recommended 	= result_list[0]['DTHR_recommended']
		self.HRHD_recommended 	= result_list[0]['HRHD_recommended']
		self.DTHRHD_recommended = result_list[0]['DTHRHD_recommended']
		
		#Playstyle -> Jumps 0 -----|----- 1 Stream
		self.playstyle = result_list[0]['playstyle']
		
		#Api settings
		self.api_key 		= result_list[0]['api_key']
		self.request_rate 	= result_list[0]['request_rate'] # Requests/min (beatmaps requests)
		
		#Money bonuses
		self.requests_max 	= result_list[0]['requests_max']
		self.donations 		= result_list[0]['donations']
		
		#Patch
		self.last_discord_patch_used 	= result_list[0]['last_discord_patch_used']
		self.last_irc_patch_used 		= result_list[0]['last_irc_patch_used']
		self.last_time_played 			= result_list[0]['last_time_played'] #timestamp
		
		connexion.close()

		return

	def save_user_profile(self, database_path):
		""" Saves the user profile into a given database """
		if not self.osu_id or not database_path:
			return

		connexion = sqlite3.connect(database_path)
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

		cursor.execute("""UPDATE users SET 
			discord_id 				= ?,
			osu_name 				= ?,
			rank 					= ?,
			accuracy_average 		= ?,
			pp_average 				= ?,
			bpm_low 				= ?,
			bpm_average 			= ?,
			bpm_high 				= ?,
			od_average 				= ?,
			ar_average 				= ?,
			cs_average 				= ?,
			len_average 			= ?,
			Nomod_playrate 			= ?,
			HR_playrate 			= ?,
			HD_playrate 			= ?,
			DT_playrate 			= ?,
			DTHD_playrate 			= ?,
			DTHR_playrate 			= ?,
			HRHD_playrate 			= ?,
			DTHRHD_playrate 		= ?,
			Nomod_recommended 		= ?,
			HR_recommended 			= ?,
			HD_recommended 			= ?,
			DTHR_recommended 		= ?,
			DTHD_recommended 		= ?,
			DTHR_recommended 		= ?, 
			HRHD_recommended 		= ?,
			playstyle 				= ?,
			api_key 				= ?,
			request_rate 			= ?,
			requests_max 			= ?,
			donations 				= ?,
			last_discord_patch_used = ?,
			last_irc_patch_used 	= ?,
			last_time_played 		= ?

			WHERE osu_id = ?
			""", data)

		connexion.commit()
		connexion.close()

		return

	def update_user_stats(self, osu_id):

		if not osu_id:
			return

		userinfo = get_user("Todo key load", osu_id, 0)
		userbest = get_user_best("Todo key load", osu_id, 0, 20)
		self.osu_name = userinfo['username']
		self.rank = int(userinfo['pp_rank'])
		self.playstyle = 0
		self.accuracy_average = 0
		self.cs_average = 0
		self.ar_average = 0
		self.od_average = 0
		self.bpm_average = []
		for score in scores:
			btmap = "Todo map load"
			pp, stars = await self.get_pyttanko(btmap, int(score['enabled_mods']), score['count300'], score['count100'], score['count50'], score['countmiss'], score['maxcombo'])
			self.accuracy_average += pyttanko.acc_calc(int(score['count300']), int(score['count100']), int(score['count50']), int(score['countmiss']))
			self.cs_average += btmap.cs
			self.ar_average += btmap.ar
			self.od_average += btmap.od
			self.bpm_average.extend([timing.ms_per_beat for timing in btmap.timing_points if timing.change])
			self.playstyle += stars.speed / stars.total
		self.playstyle = (self.playstyle / 20) * 100
		self.cs_average = self.cs_average / 20
		self.ar_average = self.ar_average / 20
		self.od_average = self.od_average / 20
		self.bpm_high = max(self.bpm_average)
		self.bpm_low = min(self.bpm_average)
		self.bpm_average = (sum(self.bpm_average) / len(self.bpm_average))
	
		return

	def print_user_profile(self):
		"""Clean output to see this user parameters"""

		if self.uso_id == None:
			print('User empty')
			return

		print("---- Global informations ----")
		print("|")
		print("|-osu_id 	 = {}".format(self.osu_id))
		print("|-uso_id 	 = {}".format(self.uso_id))
		print("|-discord_id = {}".format(self.discord_id))
		print("|-osu_name 	 = {}".format(self.osu_name))
		print("|-rank 		 = {}".format(self.rank))
		print("|")
		print("---- User performances ----")
		print("|")
		print("|-accuracy_average 	= {}".format(self.accuracy_average))
		print("|-pp_average 		= {}".format(self.pp_average))
		print("|-bpm_low 			= {}".format(self.bpm_low))
		print("|-bpm_average 		= {}".format(self.bpm_average))
		print("|-bpm_high 			= {}".format(self.bpm_high))
		print("|-od_average 		= {}".format(self.od_average))
		print("|-ar_average 		= {}".format(self.ar_average))
		print("|-cs_average 		= {}".format(self.cs_average))
		print("|-len_average 		= {}".format(self.len_average))
		print("|")
		print("---- Mods playrate ----")
		print("|")
		print("|-Nomod 	= {}%".format(self.Nomod_playrate))
		print("|-HR 		= {}%".format(self.HR_playrate))
		print("|-HD 		= {}%".format(self.HD_playrate))
		print("|-DT 		= {}%".format(self.DT_playrate))
		print("|-DTHD 		= {}%".format(self.DTHD_playrate))
		print("|-DTHR 		= {}%".format(self.DTHR_playrate))
		print("|-HRHD 		= {}%".format(self.HRHD_playrate))
		print("|-DTHRHD 	= {}%".format(self.DTHRHD_playrate))
		print("|")
		print("---- Playstyle ----")
		print("|")
		print("|-playstyle 	= {}".format(self.playstyle))
		print("|")
		print("---- Api settings ----")
		print("|")
		print("|-api_key 		= {}".format(self.api_key))
		print("|-request_rate 	= {} requests/min".format(self.request_rate))
		print("|")
		print("---- Money bonuses ----")
		print("|")
		print("|-requests_max 	= {} beatmaps/request".format(self.requests_max))
		print("|-donations 	= {}€".format(self.donations))
		print("|")
		print("---- Patch ----")
		print("|")
		print("|-last_discord_patch_used 	= {}".format(self.last_discord_patch_used))
		print("|-last_irc_patch_used 		= {}".format(self.last_irc_patch_used))
		print("|-last_time_played 			= {}".format(self.last_time_played))
		print("|")


		return

# --- Test lines !
#user.print_user_profile()
#user.od_average = 50
#user.save_user_profile("../UsoDatabase.db")