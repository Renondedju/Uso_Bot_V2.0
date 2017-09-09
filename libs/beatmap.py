# -*- coding: utf-8 -*-

import sqlite3

class Beatmap():

	def __init__(self, beatmap_id, database_path):

		self.beatmap_id = beatmap_id
		self.uso_id = None
		self.beatmapset_id = None

		self.bpm = None
		self.difficultyrating = 0
		self.aim_stars = 0
		self.speed_stars = 0

		self.playstyle = self.speed_stars/self.difficultyrating # 0 = aim (jumps) , 1 = speed (stream)

		self.diff_size = None
		self.diff_overall = None
		self.diff_approach = None
		self.diff_drain = None
		self.hit_length = None
		self.total_length = None
		self.max_combo = None

		self.artist = None
		self.creator = None
		self.title = None
		self.version = None
		self.mode = None
		self.tags = None
		self.approved = None
		self.approved_date = None
		self.last_update = None

		self.PP_100 = None
		self.PP_100_HR = None
		self.PP_100_HD = None
		self.PP_100_DT = None
		self.PP_100_DTHD = None
		self.PP_100_DTHR = None
		self.PP_100_HRHD = None
		self.PP_100_DTHRHD = None

		self.PP_99 = None
		self.PP_99_HR = None
		self.PP_99_HD = None
		self.PP_99_DT = None
		self.PP_99_DTHD = None
		self.PP_99_DTHR = None
		self.PP_99_HRHD = None
		self.PP_99_DTHRHD = None

		self.PP_98 = None
		self.PP_98_HR = None
		self.PP_98_HD = None
		self.PP_98_DT = None
		self.PP_98_DTHD = None
		self.PP_98_DTHR = None
		self.PP_98_HRHD = None
		self.PP_98_DTHRHD = None

		self.PP_97 = None
		self.PP_97_HR = None
		self.PP_97_HD = None
		self.PP_97_DT = None
		self.PP_97_DTHD = None
		self.PP_97_DTHR = None
		self.PP_97_HRHD = None
		self.PP_97_DTHRHD = None

	def load_beatmap(self, database_path):
		""" Loading a beatmap from the database """

		if not self.beatmap_id:
			return

		connexion = sqlite3.connect(database_path)
		cursor = connexion.cursor()

		query = cursor.execute("SELECT * FROM users WHERE beatmap_id = ?", [self.beatmap_id,])

		colname = [ d[0] for d in query.description ]
		result_list = [ dict(zip(colname, r)) for r in query.fetchall()]
		
		if len(result_list) == 0:
			connexion.close()
			return #No coresponding beatmap

		self.uso_id 		= result_list[0]['uso_id']
		self.beatmapset_id 	= result_list[0]['beatmapset_id']

		self.bpm 				= result_list[0]['bpm']
		self.difficultyrating 	= result_list[0]['difficultyrating']
		self.aim_stars 			= result_list[0]['aim_stars']
		self.speed_stars 		= result_list[0]['speed_stars']

		self.playstyle = self.speed_stars/self.difficultyrating

		self.diff_size 		= result_list[0]['diff_size']
		self.diff_overall 	= result_list[0]['diff_overall']
		self.diff_approach 	= result_list[0]['diff_approach']
		self.diff_drain 	= result_list[0]['diff_drain']
		self.hit_length 	= result_list[0]['hit_length']
		self.total_length 	= result_list[0]['total_length']
		self.max_combo 		= result_list[0]['max_combo']

		self.artist 		= result_list[0]['artist']
		self.creator 		= result_list[0]['creator']
		self.title 			= result_list[0]['title']
		self.version 		= result_list[0]['version']
		self.mode 			= result_list[0]['mode']
		self.tags 			= result_list[0]['tags']
		self.approved 		= result_list[0]['approved']
		self.approved_date 	= result_list[0]['approved_date']
		self.last_update 	= result_list[0]['last_update']

		self.PP_100 		= result_list[0]['PP_100']
		self.PP_100_HR 		= result_list[0]['PP_100_HR']
		self.PP_100_HD 		= result_list[0]['PP_100_HD']
		self.PP_100_DT 		= result_list[0]['PP_100_DT']
		self.PP_100_DTHD 	= result_list[0]['PP_100_DTHD']
		self.PP_100_DTHR 	= result_list[0]['PP_100_DTHR']
		self.PP_100_HRHD 	= result_list[0]['PP_100_HRHD']
		self.PP_100_DTHRHD 	= result_list[0]['PP_100_DTHRHD']

		self.PP_99 			= result_list[0]['PP_99']
		self.PP_99_HR 		= result_list[0]['PP_99_HR']
		self.PP_99_HD 		= result_list[0]['PP_99_HD']
		self.PP_99_DT 		= result_list[0]['PP_99_DT']
		self.PP_99_DTHD 	= result_list[0]['PP_99_DTHD']
		self.PP_99_DTHR 	= result_list[0]['PP_99_DTHR']
		self.PP_99_HRHD 	= result_list[0]['PP_99_HRHD']
		self.PP_99_DTHRHD 	= result_list[0]['PP_99_DTHRHD']

		self.PP_98 			= result_list[0]['PP_98']
		self.PP_98_HR 		= result_list[0]['PP_98_HR']
		self.PP_98_HD 		= result_list[0]['PP_98_HD']
		self.PP_98_DT 		= result_list[0]['PP_98_DT']
		self.PP_98_DTHD 	= result_list[0]['PP_98_DTHD']
		self.PP_98_DTHR 	= result_list[0]['PP_98_DTHR']
		self.PP_98_HRHD 	= result_list[0]['PP_98_HRHD']
		self.PP_98_DTHRHD 	= result_list[0]['PP_98_DTHRHD']

		self.PP_97 			= result_list[0]['PP_97']
		self.PP_97_HR 		= result_list[0]['PP_97_HR']
		self.PP_97_HD 		= result_list[0]['PP_97_HD']
		self.PP_97_DT 		= result_list[0]['PP_97_DT']
		self.PP_97_DTHD 	= result_list[0]['PP_97_DTHD']
		self.PP_97_DTHR 	= result_list[0]['PP_97_DTHR']
		self.PP_97_HRHD 	= result_list[0]['PP_97_HRHD']
		self.PP_97_DTHRHD 	= result_list[0]['PP_97_DTHRHD']

		connexion.close()

		return

	def save_beatmap(self, database_path):
		""" Saves a beatmap into a given database """

		if not self.discord_id:
			return

		connexion = sqlite3.connect(database_path)
		cursor = connexion.cursor()

		data = [self.uso_id,
			self.beatmapset_id,
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
			self.discord_id,]

		cursor.execute("""UPDATE users SET 
			uso_id				= ?
			beatmapset_id		= ?
			bpm					= ?
			difficultyrating	= ?
			aim_stars			= ?
			speed_stars			= ?
			playstyle			= ?
			diff_size			= ?
			diff_overall		= ?
			diff_approach		= ?
			diff_drain			= ?
			hit_length			= ?
			total_length		= ?
			max_combo			= ?
			artist				= ?
			creator				= ?
			title				= ?
			version				= ?
			mode				= ?
			tags				= ?
			approved 			= ?
			approved_date		= ?
			last_update			= ?
			PP_100 				= ?
			PP_100_HR 			= ?
			PP_100_HD 			= ?
			PP_100_DT 			= ?
			PP_100_DTHD 		= ?
			PP_100_DTHR 		= ?
			PP_100_HRHD 		= ?
			PP_100_DTHRHD 		= ?
			PP_99 				= ?
			PP_99_HR 			= ?
			PP_99_HD 			= ?
			PP_99_DT 			= ?
			PP_99_DTHD 			= ?
			PP_99_DTHR 			= ?
			PP_99_HRHD 			= ?
			PP_99_DTHRHD 		= ?
			PP_98 				= ?
			PP_98_HR 			= ?
			PP_98_HD 			= ?
			PP_98_DT 			= ?
			PP_98_DTHD 			= ?
			PP_98_DTHR 			= ?
			PP_98_HRHD 			= ?
			PP_98_DTHRHD 		= ?
			PP_97 				= ?
			PP_97_HR 			= ?
			PP_97_HD 			= ?
			PP_97_DT 			= ?
			PP_97_DTHD 			= ?
			PP_97_DTHR 			= ?
			PP_97_HRHD 			= ?
			PP_97_DTHRHD 		= ?

			WHERE discord_id 	= ?
			""", data)

		connexion.commit()
		connexion.close()

		return