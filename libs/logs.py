import json
import requests
import aiohttp
import asyncio
from datetime import datetime
from user import User

# default_payload = {
# 	'embeds' : [
# 		{
# 			'title' : 'Default embed',
# 			'description' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
# 			'color': int('0x2ecc71', 16),
# 			'author' : {
# 				'name' : 'Lorem ipsum',
# 				'icon_url' : 'https://cdn.discordapp.com/avatars/213262036069515264/4f4764137e0ff833e6cc93ca152428e4.png'
# 			},
# 			'footer' : {
# 				'text' : 'Lorem ipsum',
# 				'icon_url' : 'https://cdn.discordapp.com/avatars/213262036069515264/4f4764137e0ff833e6cc93ca152428e4.png'
# 			},
# 			'thumbnail' : {
# 				'url' : 'https://cdn.discordapp.com/avatars/213262036069515264/4f4764137e0ff833e6cc93ca152428e4.png'
# 			},
# 			'image' : {
# 				'url' : 'https://cdn.discordapp.com/avatars/213262036069515264/4f4764137e0ff833e6cc93ca152428e4.png'
# 			},
# 			'fields' : [ 
# 				{
# 					'name' : 'Lorem ipsum',
# 					'value' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
# 					'inline' : True
# 				},
# 				{
# 					'name' : 'Lorem ipsum',
# 					'value' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
# 					'inline' : True
# 				}
# 			]
# 		}
# 	]
# }

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
me = User(123, None)
me.osu_name = "Renondedju"
me.discord_name = "Renondedju"
me.rank = "MASTER"
me.discord_id = 213262036069515264
me.discord_icon = "4f4764137e0ff833e6cc93ca152428e4"
logs.add_warning_log('Some warnings')
logs.send_logs()