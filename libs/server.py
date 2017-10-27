# -*- coding: utf-8 -*-
"""
	Server library for Uso bot
	By Renondedju and Jamu
"""
import sqlite3

class Server():
	"""Server informations"""

	def __init__(self, discord_id:int, database_path:str):
		""" Init """
		#Basic parameters
		self.discord_id 	= discord_id
		self.server_name 	= None
		self.main_channel 	= None
		self.muted 			= False

		#Database
		self.database_path = database_path

		#Logs related
		self.users_count = None
		self.owner_name = None
		self.icon_url = None

		self.load_server()

	def load_server(self):
		""" Loading a server from the database """

		if not self.discord_id or not self.database_path:
			return

		#Connexion to the database
		connexion = sqlite3.connect(self.database_path)
		cursor = connexion.cursor()
		
		query = cursor.execute("SELECT * FROM servers WHERE discord_id = ?", [self.discord_id,])

		#Making a cool looking dictionary
		colname = [ d[0] for d in query.description ]
		result_list = [ dict(zip(colname, r)) for r in query.fetchall()]

		if len(result_list) == 0:
			connexion.close()
			return #No coresponding user

		self.discord_id 	= result_list[0]['discord_id']
		self.server_name 			= result_list[0]['server_name']
		self.main_channel 	= result_list[0]['main_channel']
		self.muted 			= result_list[0]['muted']

		connexion.close()

		return

	def save_server(self):
		""" Saves the server into a given database """
		if not self.discord_id or not self.database_path:
			return

		#Connexion to the database
		connexion = sqlite3.connect(self.database_path)
		cursor = connexion.cursor()

		data = [self.server_name,
				self.main_channel,
				self.muted,
				self.discord_id,]

		cursor.execute("""UPDATE servers SET 
			server_name = ?,
			main_channel = ?,
			muted = ?

			WHERE discord_id = ?
			""", data)

		connexion.commit()
		connexion.close()

		return

	def print_server(self):
		"""Clean output to see this server parameters"""

		if self.server_name == None:
			print('Server empty')
			return

		print("---- Global informations ----")
		print("|")
		print("|-discord_id 	= {}".format(self.discord_id))
		print("|-server_name 	= {}".format(self.server_name))
		print("|-muted 		= {}".format(self.muted))
		print("|-main_channel 	= {}".format(self.main_channel))
		print("|")

		return

# --- Test lines !
#server = Server(54, "../UsoDatabase.db")
#server.print_server()
#server.main_channel = 5054154161584151
#server.save_server("../UsoDatabase.db")