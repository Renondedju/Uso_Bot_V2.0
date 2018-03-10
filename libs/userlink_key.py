from __main__ import *

import time
import string
import random

from libs.user import User

class key(object):
	""" Secret key object """

	def __init__(self, size=6, validity=600):
		self.__key = ''.join(random.SystemRandom().choice(
			string.ascii_uppercase + string.digits) for _ in range(size))
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

	def generate_new_key(self, osu_id: int, discord_id: int):
		""" Generating a new key """
		discord_id = int(discord_id)

		link_dictionary[osu_id] = [key(), discord_id]

		# Creating the user
		user = User(osu_id)

		return link_dictionary[osu_id][0].get()

	def link_account(self, osu_id: int, key: string):
		""" Trys to link an account """

		# Creating the user
		user = User(osu_id=osu_id)
		
		str_id = str(osu_id)

		if link_dictionary[str_id][0].get() == key:
			# The key is right : linking user
			user.discord_id = link_dictionary[str_id][1]
			user.save_user_profile()
			return

		elif link_dictionary[str_id][0].get() == None:
			# This key seems to be expired
			link_dictionary.pop(str_id)
			raise ValueError("The key you are looking for expired")

		else:
			raise KeyError("This key doesn't exists")
