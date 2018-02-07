import asyncio, sys, re, os, time

sys.path.append(os.path.realpath('../'))

from libs.osuapi         import *
from libs.user           import User
from libs.beatmap        import Beatmap
from libs.preset         import Preset
from libs.recommendation import REngine
from libs                import pyttanko

info  = sys.stdout.write
error = sys.stderr.write

class IRCbot:
    def __init__(self, bot):
        self.bot = bot
        self.nick = self.bot.settings['irc_username'] # ?
        self.passw = self.bot.settings['irc_token'] # ?
        self.buffer = {}
        loop = asyncio.get_event_loop()
        loop.create_task(self.client())

    async def send_message(self, target, msg):
        '''Processes messages to prevent spam'''
        if target not in self.buffer:
            # I guess since this is the first message to this user we can
            # Just send it immediately after adding them to the buffer
            self.buffer[target] = {
                'messages': [], 'timer': time.time(),
                'last_msg': time.time(), 'nb_msg': 1}
            self.send(target, msg)
        else:
            now = time.time()
            if now - self.buffer[target]['last_msg'] >= 8:
                self.buffer[target]['timer'] = now
                self.buffer[target]['nb_msg'] = 0
            if now - self.buffer[target]['last_msg'] >= 1 and self.buffer[target]['nb_msg'] <= 5:
                self.send(target, msg)
                self.buffer[target]['nb_msg'] += 1
                self.buffer[target]['last_msg'] = time.time()
            else: self.buffer[target]['messages'].append(msg)

    async def check_buffer(self): # Is there a way to compress these two into one function, since they're mostly the same?
        '''Processes buffer and sends any messages that are able to be sent now'''
        for target in self.buffer.copy():
            if len(self.buffer[target]['messages']) == 0:
                self.buffer.pop(target)
                continue
            now = time.time() # I'd put this outside the loop, but what if there's a lot of messages :^)
            if now - self.buffer[target]['last_msg'] >= 8:
                self.buffer[target]['timer'] = now
                self.buffer[target]['nb_msg'] = 0
            if now - self.buffer[target]['last_msg'] >= 1 and self.buffer[target]['nb_msg'] <= 5:
                msg = self.buffer[target]['messages'].pop(0)
                self.send(target, msg)
                self.buffer[target]['nb_msg'] += 1
                self.buffer[target]['last_msg'] = now

    def send(self, target, msg):
        '''Sends a private message to the target'''
        self.writer.write(f'PRIVMSG {target} {msg}\n'.encode())
        info(f'To {target}: {msg}\n') # So we can see the messages sent

    def pong(self, msg):
        '''Responds to pings sent by the IRC server'''
        self.writer.write(f'PONG {msg[-1]}\n'.encode())
        # So we know it's still connected during debugging
        info('My heart fluttered.\n')

    async def get_text(self):
        '''Recieve, split, and parse data coming from the irc server'''
        messages = []
        data = await self.reader.read(2048)
        if not data:
            await self.reconnect()
            return messages
        text = data.decode('utf-8')
        for line in text.split('\n'):
            if line.strip() != '':
                parsed = self.parse_line(line)
                if parsed[1] == 'PING': self.pong(parsed)
                # This is so we don't process these, as there are a lot of them
                elif parsed[1] != 'QUIT': messages.append(parsed)
        return messages

    def parse_line(self, line):
        '''Parse lines of data with regex'''
        parsed = re.findall('^(?:[:](\S+) )?(\S+)(?: (?!:)(.+?))?(?: [:](.+))?$', line)
        try: return parsed[0] # Don't judge this, I just want to see why it randomly crashes sometimes xd
        except: info(line); return ('', '', '', '')

    async def connect(self):
        '''Connects and logs into the IRC server'''
        self.reader, self.writer = await asyncio.open_connection('irc.ppy.sh', 6667, ssl=False)
        info('Connected to Bancho.\n')
        self.writer.write(f'USER {self.nick} {self.nick} {self.nick} :Test bot\n'.encode())
        self.writer.write(f'PASS {self.passw}\n'.encode())
        self.writer.write(f'NICK {self.nick}\n'.encode())

    async def reconnect(self):
        '''I'm hoping this makes reconnecting easy'''
        info('Reconnecting...')
        await self.close()
        await self.connect()

    async def close(self):
        '''I guess this is to properly handle closing the connection?'''
        self.writer.close()

    async def client(self):
        '''The actual bot'''
        engine = REngine()
        await self.connect()
        try: # Might add certain handlers for these in the future
            while self == self.bot.get_cog('IRCbot'):
                for msg in await self.get_text():
                    if msg[1] == 'PRIVMSG':
                        sender = msg[0].split('!')[0]
                        info(f'From {sender}: {msg[3]}\n')
                        if msg[3].split(' ')[0] == 'o!r':
                            # TODO make option parsing function
                            count = 1
                            engine.recommend(User(sender), count)
                            for i in range(count):
                                bmap = engine.recommendatons[i]
                                mods = self.process_mods(engine.mods[i], bmap)
                                await self.send_message(sender, self.build_map(mods, bmap))
                        elif msg[3] == 'o!recent':
                            await self.send_message(sender, 'This is a #TODO')
                        elif msg[3].split(' ')[0] == 'o!verify':
                            # TODO add memcache check for keys
                            await self.send_message(sender, 'This is a #TODO')
                        else: # No commands so check for maps
                            for mapid in re.findall('https://osu.ppy.sh/b/([0-9]*)', msg[3]):
                                # TODO add regex for mods
                                bmap = Beatmap(mapid)
                                mods = self.process_mods('', bmap)
                                await self.send_message(sender, self.build_map(mods, bmap))
                    elif msg[1] in ['001', '372', '375', '376']:
                        info(f'{msg[3].strip()}\n')
                    elif msg[1] in ['311', '319', '312', '318', '401']:
                        info(f'Whois {msg[2].split(" ")[1]}: {msg[3].strip()}\n')
                    elif msg[1] == '464':
                        error('Bad authentication token.\n')
                        self.close()
                    else: info(str(msg)) # So we can see if we aren't parsing something we need to be
                await self.check_buffer()
            else: await self.close()
        except KeyboardInterrupt:
            await self.close()

    def build_map(self, mods, bmap):
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

    def process_mods(self, mods, bmap):
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
            modinfos = {
                'mods': f'+{mods}',
                'time': '{}:{}'.format(int(mins), int(secs)),
                'pp_100': getattr(bmap, f'PP_100_{mods}'),
                'pp_99': getattr(bmap, f'PP_99_{mods}'),
                'pp_98': getattr(bmap, f'PP_98_{mods}'),
                'pp_97': getattr(bmap, f'PP_97_{mods}')
            }
        return modinfos

def setup(bot):
    bot.add_cog(IRCbot(bot))