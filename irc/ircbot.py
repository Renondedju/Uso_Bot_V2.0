# -*- coding: utf-8 -*-
from irc import IRCbot
import re, os, sys

sys.path.append(os.path.realpath('../'))

from libs.user           import User
from libs.beatmap        import Beatmap
from libs.recommendation import REngine

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

settings = json.loads(open('../config.json', 'r').read())
irc = IRCbot('irc.ppy.sh', settings['irc_username'], settings['irc_token'])
irc.connect()
engine = REngine()
stayonline = True

try: # Might add certain handlers for these in the future
    while stayonline == True:
        for msg in irc.get_text():
            if msg[1] == 'PRIVMSG':
                sender = msg[0].split('!')[0]
                print(f'From {sender}: {msg[3]}')
                if msg[3].split(' ')[0] == 'o!r':
                    # TODO make option parsing function
                    count = 1
                    engine.recommend(User(sender), count)
                    for i in range(count):
                        bmap = engine.recommendatons[i]
                        mods = process_mods(engine.mods[i], bmap)
                        irc.send_message(sender, build_map(mods, bmap))
                elif msg[3] == 'o!recent':
                    irc.send_message(sender, 'This is a #TODO')
                elif msg[3].split(' ')[0] == 'o!verify':
                    # TODO add memcache check for keys
                    irc.send_message(sender, 'This is a #TODO')
                else: # No commands so check for maps
                    for mapid in re.findall('https://osu.ppy.sh/b/([0-9]*)', msg[3]):
                        # TODO add regex for mods
                        bmap = Beatmap(mapid)
                        mods = process_mods('', bmap)
                        irc.send_message(sender, build_map(mods, bmap))
            elif msg[1] in ['001', '372', '375', '376']:
                print(msg[3].strip())
            elif msg[1] in ['311', '319', '312', '318', '401']:
                print(f'Whois {msg[2].split(" ")[1]}: {msg[3].strip()}')
            elif msg[1] == '464':
                print('Bad authentication token.')
                stayonline = False
                break
            else: print(msg) # So we can see if we aren't parsing something we need to be
        irc.check_buffer()
    else: irc.close()
except KeyboardInterrupt:
    irc.close()