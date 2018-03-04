# Uso startup file

import sys
import json
import time

sys.path.insert(0, './discord')
sys.path.insert(0, './irc')
sys.path.insert(0, './api')

#Configs
config_path = './config.json'
settings    = json.loads(open(config_path, 'r').read())

#Userlink key thats an optimisation todo
link_dictionary = {}

from libs.logs import Log
from threading import Thread

#Logs
logs = Log()

import discord_bot
import irc_bot
import api_bot


#Logs thread
run_log_thread = True

#Logs thread function
def send_logs():
    """ Sending logs every 10 Sec to avoid slowing down commands """
    print('Running log thread ..')
    
    while run_log_thread:
        try:
            time.sleep(10)
            logs.send_logs()
        except:
            pass
    
    print('Terminated log thread !')
    return

def discord_th():
    print('Running discord thread ..')
    discord_bot.run_discord()
    print('Terminated discord thread !')
    return

def irc_th():
    print('Running irc thread ..')
    irc_bot.run_irc()
    print('Terminated irc thread !')
    return


logs_thread    = Thread(target=send_logs)
irc_thread     = Thread(target=irc_th)

logs_thread.start()
irc_thread.start()
discord_bot.run_discord()

irc_thread.join()
run_log_thread = False
logs_thread.join()

print('USO BOT HAS BEEN TERMINATED !')