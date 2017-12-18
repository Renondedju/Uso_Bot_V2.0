import time
import string
import random
import memcache
import update_stats
import sqlite3
from osuapi import OsuApi, ReqConnector
import constants

class key(object):

	def __init__(self, size = 6, validity = 600):
		self.__key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))
		self.__validity = validity
		self.__creation_time = time.time()

	def get(self):

		if time.time() - self.__creation_time <= self.__validity:
			return self.__key
		else:
			self.__key = None
			return None

	def invalidate(self):
		self.__key = None

class userlink:

	def __init__(self, database_connexion):
		self.shared = memcache.Client(['127.0.0.1:11211'], debug=0)
		self.keys = {} # Osu id : [Key, Discord Id]
		self.shared.set('keys', self.keys)
		self.database_connexion = database_connexion
		self.database_cursor = database_connexion.cursor()
		self.api = OsuApi(constants.Api.osuApiKey, connector=ReqConnector())

	def generate_new_key(self, osu_id, discord_id):

		discord_id = int(discord_id)

		self.keys = self.shared.get('keys')
		self.keys[osu_id] = [key(), discord_id]
		self.shared.set('keys', self.keys)

		return self.keys[osu_id][0].get()

	def link_account(self, osu_id, key, osu_name):

		osu_id = int(osu_id)

		self.keys = self.shared.get('keys')
		self.database_cursor.execute("SELECT * FROM users WHERE osuId = ?", (osu_id,))

		if not self.database_cursor.fetchall():
			self.database_cursor.execute("INSERT INTO users (osuId, osuName) VALUES (?)", (osu_id, osu_name,))
			self.database_connexion.commit()

		if self.keys[osu_id][0].get() == key:
			self.database_cursor.execute("UPDATE users SET discordId = ?, rank = ? WHERE osuId = ?", (self.keys[osu_id][1], "USER", osu_id,))
			self.database_connexion.commit()
			update_stats.update_stats(self.keys[osu_id][1], self.database_connexion, self.api)
			return
			
		elif self.keys[osu_id][0].get() == None:
			self.keys.pop(osu_id)
			self.shared.set('keys', self.keys)
			raise ValueError("The key you are looking for expired")

		else:
			raise ValueError("This key doesn't exists")