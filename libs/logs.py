# -*- coding: utf-8 -*-
"""

	Logging system for uso bot
	By Renondedju and Jamu

"""

from __main__ import *

import os
import sys
import json
import requests

sys.path.append(os.path.realpath('../'))

from libs.user     import User
from libs.server   import Server
from datetime      import datetime


class Log():
    """ Logs system """

    def __init__(self):
        """ Init """

        self.settings = settings
        self.payload  = {'embeds': []}

    def add_log(self, user, description):
        """ Adding a simple log to the payloads """

        new_payload = {

            'description': description,
            'color': 0,

            'author': {
                'name': '{}'.format(user.osu_name if not user.discord_name else user.discord_name),
                'icon_url': 'https://cdn.discordapp.com/avatars/{}/{}.png'.format(user.discord_id, user.discord_icon)
            },
            'footer': {
                'text': datetime.now().strftime('%Y/%m/%d at %H:%M:%S')
            }
        }

        self.payload['embeds'].append(new_payload)

        return self.payload['embeds'].index(new_payload)

    def add_error_log(self, user, description, error):
        """ Adding a simple log to the payloads """

        new_payload = {

            'description': '{}\n```{}```'.format(description, (error[:1800] + '...') if len(error) > 75 else error),
            'color': int("0xe74c3c", 16),

            'author': {
                'name': '{}'.format(user.osu_name if not user.discord_name else user.discord_name),
                'icon_url': 'https://cdn.discordapp.com/avatars/{}/{}.png'.format(user.discord_id, user.discord_icon)
            },
            'footer': {
                'text': datetime.now().strftime('%Y/%m/%d at %H:%M:%S')
            }
        }

        self.payload['embeds'].append(new_payload)

        return self.payload['embeds'].index(new_payload)

    def add_warning_log(self, warning):
        """ Adding a simple log to the payloads """

        new_payload = {

            'description': '**{}**'.format(warning),
            'color': int('0xf1c40f', 16),

            'author': {
                'name': 'Uso! - BOT',
                'icon_url': 'https://cdn.discordapp.com/avatars/318357311951208448/8c753cebbac3481fd90485087eaf20df.webp?size=256'
            },
            'footer': {
                'text': datetime.now().strftime('%Y/%m/%d at %H:%M:%S')
            }
        }

        self.payload['embeds'].append(new_payload)

        return self.payload['embeds'].index(new_payload)

    def add_server_log(self, action, server):
        """ Adding a simple log to the payloads """

        new_payload = {

            'description': "**A server __{}__ the bot.**\n".format(action) +
            "__Server name :__ **{}**\n".format(server.server_name) +
            "__Server ID :__ **{}**\n".format(server.discord_id) +
            "__Users count :__ **{}**\n".format(server.users_count) +
            "__Owner name :__ **{}**".format(
                server.owner_name),
            'color': int('0x3498db', 16),

            'author': {
                'name': 'Uso! - BOT',
                'icon_url': 'https://cdn.discordapp.com/avatars/318357311951208448/8c753cebbac3481fd90485087eaf20df.webp?size=256'
            },
            'footer': {
                'text': datetime.now().strftime('%Y/%m/%d at %H:%M:%S')
            },
            'thumbnail': {
                'url': server.icon_url
            }
        }

        self.payload['embeds'].append(new_payload)

        return self.payload['embeds'].index(new_payload)

    def add_debug_log(self, debug):
        """ Adding a debug log to the payloads """

        new_payload = {

            'description': '**{}**'.format(debug),
            'color': int('0x2c2f33', 16),

            'author': {
                'name': 'Uso! - BOT',
                'icon_url': 'https://cdn.discordapp.com/avatars/318357311951208448/8c753cebbac3481fd90485087eaf20df.webp?size=256'
            },
            'footer': {
                'text': datetime.now().strftime('%Y/%m/%d at %H:%M:%S')
            }
        }

        self.payload['embeds'].append(new_payload)

        return self.payload['embeds'].index(new_payload)

    def send_logs(self):
        """ Sending logs """

        #Sending logs
        response = requests.post(
            self.settings['webhook_url'], data=json.dumps(self.payload),
            headers={'Content-Type': 'application/json'}
        )

        #Writing logs into the logs file
        logs_file = open(self.settings['logs_file'], 'a+')

        for embed in self.payload['embeds']:
            line =  '\n' + embed['footer']['text'] + '\n' #Date
            line += " - " + embed['description']          #Log description
            logs_file.write(line + '\n')
        
        logs_file.close()

        # Every log has been send so reseting the payload
        self.payload = {'embeds': []}

        return response.status_code


if __name__ == '__main__':
    # Test code
    logs = Log()
    logs.add_debug_log('Example logs are following ...')
    logs.send_logs()
    logs.add_warning_log('Starting irc script')
    logs.add_debug_log('Connecting to irc.ppy.sh:6667')
    logs.send_logs()
    logs.add_debug_log('Connected !')
    logs.send_logs()
