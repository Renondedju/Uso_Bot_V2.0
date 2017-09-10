import json
import requests
from datetime import datetime
from user import User
from server import Server

class Log():

	def __init__(self):

		self.settings = json.loads(open('../config.json', 'r').read())
		self.payload = { 'embeds' : [] }

	def add_log(self, user, description):
		""" Adding a simple log to the payloads """

		new_payload = {
			
			'description' : description,
			'color': 0,

			'author' : {
				'name' : '{} - {}'.format(user.osu_name if not user.discord_name else user.discord_name, user.rank.upper()),
				'icon_url' : 'https://cdn.discordapp.com/avatars/{}/{}.png'.format(user.discord_id, user.discord_icon)
			},
			'footer' : {
				'text' : datetime.now().strftime('%Y/%m/%d at %H:%M:%S')
			}
		}

		self.payload['embeds'].append(new_payload)

		return self.payload['embeds'].index(new_payload)

	def add_error_log(self, user, description, error):
		""" Adding a simple log to the payloads """

		new_payload = {
			
			'description' : '{}\n```{}```'.format(description, (error[:1800] + '...') if len(error) > 75 else error),
			'color': int("0xe74c3c", 16),

			'author' : {
				'name' : '{} - {}'.format(user.osu_name if not user.discord_name else user.discord_name, user.rank.upper()),
				'icon_url' : 'https://cdn.discordapp.com/avatars/{}/{}.png'.format(user.discord_id, user.discord_icon)
			},
			'footer' : {
				'text' : datetime.now().strftime('%Y/%m/%d at %H:%M:%S')
			}
		}

		self.payload['embeds'].append(new_payload)

		return self.payload['embeds'].index(new_payload)

	def add_warning_log(self, warning):
		""" Adding a simple log to the payloads """

		new_payload = {
			
			'description' : '**{}**'.format(warning),
			'color': int('0xf1c40f', 16),

			'author' : {
				'name' : 'Uso! - BOT',
				'icon_url' : 'https://cdn.discordapp.com/avatars/318357311951208448/8c753cebbac3481fd90485087eaf20df.webp?size=256'
			},
			'footer' : {
				'text' : datetime.now().strftime('%Y/%m/%d at %H:%M:%S')
			}
		}

		self.payload['embeds'].append(new_payload)

		return self.payload['embeds'].index(new_payload)

	def add_server_log(self, action, server):
		""" Adding a simple log to the payloads """

		new_payload = {
			
			'description' : "**A server __{}__ the bot.**\n".format(action) + 
							"__Server name :__ **{}**\n".format(server.server_name) + 
							"__Server ID :__ **{}**\n".format(server.discord_id) + 
							"__Users count :__ **{}**\n".format(server.users_count) + 
							"__Owner name :__ **{}**".format(server.owner_name),
			'color': int('0x3498db', 16),

			'author' : {
				'name' : 'Uso! - BOT',
				'icon_url' : 'https://cdn.discordapp.com/avatars/318357311951208448/8c753cebbac3481fd90485087eaf20df.webp?size=256'
			},
			'footer' : {
				'text' : datetime.now().strftime('%Y/%m/%d at %H:%M:%S')
			},
			'thumbnail' : {
 				'url' : server.icon_url
 			}
		}

		self.payload['embeds'].append(new_payload)

		return self.payload['embeds'].index(new_payload)

	def send_logs(self):
		""" Sending logs """

		response = requests.post(
			self.settings['webhookUrl'], data=json.dumps(self.payload),
			headers={'Content-Type': 'application/json'}
		)

		#Every log has been send so reseting the payload
		self.payload = { 'embeds' : [] }

		return response.status_code

logs = Log()
server = Server(310348632094146570, None)
server.icon_url = 'https://cdn.discordapp.com/avatars/213262036069515264/4f4764137e0ff833e6cc93ca152428e4.png'
server.owner_name = 'Renondedju'
server.users_count = 123456789
server.server_name = 'Just a test'
logs.add_server_log('removed', server)
logs.send_logs()