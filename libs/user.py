import sqlite3

class User():
	""" User informations """

	def __init__(self, discord_id, osu_id, database_path):
		#Global informations
		self.uso_id = uso_id
		self.discord_id = discord_id
		self.osu_id = osu_id
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

		load_user_profile(database_path)

	def load_user_profile(self, database_path):
		""" Loading a user profile from the database """

		self.connexion = sqlite3.connect(database_path)
		self.cursor = connexion.cursor()

		if not osu_id:
			return	

		self.cursor.execute("SELECT * FROM users WHERE osu_id = ?", [osu_id,])
		#TODO
		return

	def save_user_profile(self, database_path):
		""" Saves the user profile into a given database """
		print ("nothing for now ...")
		#TODO