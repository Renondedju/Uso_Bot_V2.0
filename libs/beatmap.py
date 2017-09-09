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

	

"""
uso_id
beatmap_id
beatmapset_id

bpm
difficultyrating (stars)
aim_stars
speed_stars

playstyle = speed/difficultyrating # 0 = aim (jumps) , 1 = speed (stream)

diff_size
diff_overall
diff_approach
diff_drain
hit_length
total_length
max_combo

artist
creator
title
version
mode
tags
approved
approved_date
last_update

100_PP
100_HR_PP
100_HD_PP
100_DT_PP
100_DTHD_PP
100_DTHR_PP
100_HRHD_PP
100_DTHRHD_PP

99_PP
99_HR_PP
99_HD_PP
99_DT_PP
99_DTHD_PP
99_DTHR_PP
99_HRHD_PP
99_DTHRHD_PP

98_PP
98_HR_PP
98_HD_PP
98_DT_PP
98_DTHD_PP
98_DTHR_PP
98_HRHD_PP
98_DTHRHD_PP

97_PP
97_HR_PP
97_HD_PP
97_DT_PP
97_DTHD_PP
97_DTHR_PP
97_HRHD_PP
97_DTHRHD_PP
"""