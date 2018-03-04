# -*- coding: utf-8 -*-
from __main__ import *

from irc import IRCbot
import re, os, sys, traceback

sys.path.append(os.path.realpath('../'))

from datetime            import datetime
from libs.user           import User
from libs.beatmap        import Beatmap
from libs.recommendation import REngine

from commands.test import *
from commands.help import *

def build_map(mods, bmap):
    mapinfos  =  '\x01ACTION'
    mapinfos += f' [https://osu.ppy.sh/b/{bmap.beatmap_id}'
    mapinfos += f' {bmap.title}[{bmap.version}] {mods["mods"]}]'
    mapinfos += f' ▸ 97%: {mods["pp_97"]}'
    mapinfos += f' ▸ 98%: {mods["pp_98"]}'
    mapinfos += f' ▸ 99%: {mods["pp_99"]}'
    mapinfos += f' ▸ 100%: {mods["pp_100"]}'
    mapinfos += f' ▸ {mods["time"]}♪ ▸ {bmap.difficultyrating}★'
    mapinfos += f' ▸ {bmap.bpm}BPM ▸ AR: {bmap.diff_approach}'
    mapinfos += f' ▸ CS: {bmap.diff_size} ▸ OD: {bmap.diff_overall}'
    mapinfos += f' ▸ HP: {bmap.diff_drain}\x01'
    return mapinfos

def process_mods(mods, bmap):
    if mods == '':
        mins, secs = divmod(bmap.hitobjects[-1].time / 1000, 60)
        modinfos = {
            'mods': '',
            'time': '{}:{}'.format(int(mins), int(secs)),
            'pp_100': bmap.PP_100,
            'pp_99': bmap.PP_99,
            'pp_98': bmap.PP_98,
            'pp_97': bmap.PP_97
        }
    else:
        # This should work in theory xd
        if 'DT' in mods or 'NC' in mods: speed_mult = 1.5
        elif 'HT' in mods: speed_mult = 0.75
        else: speed_mult = 1
        mins, secs = divmod((bmap.hitobjects[-1].time / speed_mult) / 1000, 60)
        modinfo = {
            'mods': f'+{mods}',
            'time': '{}:{}'.format(int(mins), int(secs)),
            'pp_100': getattr(bmap, f'PP_100_{mods}'),
            'pp_99': getattr(bmap, f'PP_99_{mods}'),
            'pp_98': getattr(bmap, f'PP_98_{mods}'),
            'pp_97': getattr(bmap, f'PP_97_{mods}')
        }
    return modinfos

def run_irc():
    irc = IRCbot('irc.ppy.sh', settings['irc_username'], settings['irc_token'])
    engine = REngine()
    stayonline = True

    logs.add_warning_log('Connecting to irc.ppy.sh:6667 as ' + irc.nick)
    logs.send_logs()

    irc.connect()    

    while stayonline:
        try:
            message = irc.get_privmsg()
            if (message[0]): #if we got a message
                print('From ' + message[1]['sender'] + ' : ' + message[1]['message'])
                user = User(osu_name=message[1]['sender'])
                logs.add_log(user, 'IRC : ' + message[1]['message'])

                #checking if the message is a command
                if (message[1]['message'].startswith(settings['prefix'])):
                    command_text = message[1]['message'].strip(settings['prefix']).split(' ')[0]

                    if (command_text == 'test'):
                        irc_command_test(irc, user)
                    if (command_text == 'help'):
                        irc_command_help(irc, user)

            #Checking buffer and sending messages if needed
            irc.check_buffer()

        except KeyboardInterrupt:
            irc.close()

        except Exception as e:
            ex_type, ex, tb = sys.exc_info()
            errors = traceback.format_tb(tb)
            date   = datetime.now().strftime('%Y/%m/%d at %H:%M:%S')

            errorReport = '\n\n---ERROR REPORT---  ' + date + '\n'
            for error in errors:
                errorReport += error
            errorReport += '{0} : {1}'.format(type(ex).__name__, ex.args)
            
            logs.add_error_log(User(osu_name=message[1]['sender']), message[1]['message'], errorReport)
            irc.send_message(message[1]['sender'], 'Damn ! An error ! I created a report, this should be fixed soon :)')
            print (errorReport)


    irc.close()

    logs.add_warning_log('IRC connexion closed')
    logs.send_logs()