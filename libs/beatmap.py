# -*- coding: utf-8 -*-

import sqlite3

class Beatmap():

	def __init__(self, beatmap_id, database_path):

		self.beatmap_id = beatmap_id
		self.uso_id = result_list[0]['test']
		self.beatmapset_id = result_list[0]['test']

		self.bpm = result_list[0]['test']
		self.difficultyrating = 0
		self.aim_stars = 0
		self.speed_stars = 0

		self.playstyle = self.speed_stars/self.difficultyrating # 0 = aim (jumps) , 1 = speed (stream)

		self.diff_size = result_list[0]['test']
		self.diff_overall = result_list[0]['test']
		self.diff_approach = result_list[0]['test']
		self.diff_drain = result_list[0]['test']
		self.hit_length = result_list[0]['test']
		self.total_length = result_list[0]['test']
		self.max_combo = result_list[0]['test']

		self.artist = result_list[0]['test']
		self.creator = result_list[0]['test']
		self.title = result_list[0]['test']
		self.version = result_list[0]['test']
		self.mode = result_list[0]['test']
		self.tags = result_list[0]['test']
		self.approved = result_list[0]['test']
		self.approved_date = result_list[0]['test']
		self.last_update = result_list[0]['test']

		self.PP_100 = result_list[0]['test']
		self.PP_100_HR = result_list[0]['test']
		self.PP_100_HD = result_list[0]['test']
		self.PP_100_DT = result_list[0]['test']
		self.PP_100_DTHD = result_list[0]['test']
		self.PP_100_DTHR = result_list[0]['test']
		self.PP_100_HRHD = result_list[0]['test']
		self.PP_100_DTHRHD = result_list[0]['test']

		self.PP_99 = result_list[0]['test']
		self.PP_99_HR = result_list[0]['test']
		self.PP_99_HD = result_list[0]['test']
		self.PP_99_DT = result_list[0]['test']
		self.PP_99_DTHD = result_list[0]['test']
		self.PP_99_DTHR = result_list[0]['test']
		self.PP_99_HRHD = result_list[0]['test']
		self.PP_99_DTHRHD = result_list[0]['test']

		self.PP_98 = result_list[0]['test']
		self.PP_98_HR = result_list[0]['test']
		self.PP_98_HD = result_list[0]['test']
		self.PP_98_DT = result_list[0]['test']
		self.PP_98_DTHD = result_list[0]['test']
		self.PP_98_DTHR = result_list[0]['test']
		self.PP_98_HRHD = result_list[0]['test']
		self.PP_98_DTHRHD = result_list[0]['test']

		self.PP_97 = result_list[0]['test']
		self.PP_97_HR = result_list[0]['test']
		self.PP_97_HD = result_list[0]['test']
		self.PP_97_DT = result_list[0]['test']
		self.PP_97_DTHD = result_list[0]['test']
		self.PP_97_DTHR = result_list[0]['test']
		self.PP_97_HRHD = result_list[0]['test']
		self.PP_97_DTHRHD = result_list[0]['test']

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

