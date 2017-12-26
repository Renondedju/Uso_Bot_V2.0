import time
import string
import random
import memcache

from libs.user import User

class key(object):
	""" Secret key object """
	def __init__(self, size = 6, validity = 600):
		self.__key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))
		self.__validity = validity
		self.__creation_time = time.time()

	def get(self):
		""" Get method """
		if time.time() - self.__creation_time <= self.__validity:
			return self.__key
		else:
			self.__key = None
			return None

	def invalidate(self):
		""" Invalidating the key """
		self.__key = None

class userlink:

	def __init__(self, database_connexion):
		self.shared = memcache.Client(['127.0.0.1:11211'], debug=0)
		self.keys = {} # Osu id : [Key, Discord Id]
		self.shared.set('keys', self.keys)

	def generate_new_key(self, osu_id, discord_id):
		""" Generating a new key """
		discord_id = int(discord_id)

		self.keys = self.shared.get('keys')
		self.keys[osu_id] = [key(), discord_id]
		self.shared.set('keys', self.keys)

		return self.keys[osu_id][0].get()

	def link_account(self, osu_id: int, key: string, osu_name: string):
		""" Trys to link an account """

		#Updating the keys cache
		self.keys = self.shared.get('keys')
		#Creating the user
		user = User(osu_id)

		if self.keys[osu_id][0].get() == key:
			# The key is right : linking user
			user.discord_id = self.keys[osu_id][1]
			user.save_user_profile()
			return
			
		elif self.keys[osu_id][0].get() == None:
			# This key seems to be expired
			self.keys.pop(osu_id)
			self.shared.set('keys', self.keys)
			raise ValueError("The key you are looking for expired")

		else:
			raise ValueError("This key doesn't exists")