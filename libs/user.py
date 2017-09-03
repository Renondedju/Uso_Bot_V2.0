import sqlite3

class User():
	""" User informations """

	def __init__(self, osu_id, database_path):
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

	def load_user_profile(self, database_path):
		""" Loading a user profile from the database """
		if not self.osu_id:
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
		
		print(result_list)
		
		self.uso_id = result_list[0]['uso_id']
		self.discord_id = result_list[0]['discord_id']
		self.osu_name = result_list[0]['osu_name']
		self.rank = result_list[0]['rank']
		
		#User performances
		self.accuracy_average = result_list[0]['accuracy_average']
		self.pp_average = result_list[0]['pp_average']
		self.bpm_low = result_list[0]['bpm_low']
		self.bpm_average = result_list[0]['bpm_average']
		self.bpm_high = result_list[0]['bpm_high']
		self.od_average = result_list[0]['od_average']
		self.ar_average = result_list[0]['ar_average']
		self.cs_average = result_list[0]['cs_average']
		self.len_average = result_list[0]['len_average'] #Drain
		
		#Mods playrate
		self.Nomod_playrate = result_list[0]['Nomod_playrate']
		self.HR_playrate = result_list[0]['HR_playrate']
		self.HD_playrate = result_list[0]['HD_playrate']
		self.DT_playrate = result_list[0]['DT_playrate']
		self.DTHD_playrate = result_list[0]['DTHD_playrate']
		self.DTHR_playrate = result_list[0]['DTHR_playrate']
		self.HRHD_playrate = result_list[0]['HRHD_playrate']
		self.DTHRHD_playrate = result_list[0]['DTHRHD_playrate']
		
		#Mods recommended
		self.Nomod_recommended = result_list[0]['Nomod_recommended']
		self.HR_recommended = result_list[0]['HR_recommended']
		self.HD_recommended = result_list[0]['HD_recommended']
		self.DT_recommended = result_list[0]['DT_recommended']
		self.DTHD_recommended = result_list[0]['DTHD_recommended']
		self.DTHR_recommended = result_list[0]['DTHR_recommended']
		self.HRHD_recommended = result_list[0]['HRHD_recommended']
		self.DTHRHD_recommended = result_list[0]['DTHRHD_recommended']
		
		#Playstyle -> Jumps 0 -----|----- 1 Stream
		self.playstyle = result_list[0]['playstyle']
		
		#Api settings
		self.api_key = result_list[0]['api_key']
		self.request_rate = result_list[0]['request_rate'] # Requests/min (beatmaps requests)
		
		#Money bonuses
		self.requests_max = result_list[0]['requests_max']
		self.donations = result_list[0]['donations']
		
		#Patch
		self.last_discord_patch_used = result_list[0]['last_discord_patch_used']
		self.last_irc_patch_used = result_list[0]['last_irc_patch_used']
		self.last_time_played = result_list[0]['last_time_played'] #timestamp
		
		
		connexion.close()

		return

	def save_user_profile(self, database_path):
		""" Saves the user profile into a given database """
		print ("nothing for now ...")
		#TODO


user = User(54, "../UsoDatabase.db")