# -*- coding: utf-8 -*-
import re, os, sys
import socket, time

class IRCbot:
    def __init__(self, server, nick, passw):
        self.server = server
        self.nick = nick
        self.passw = passw
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.messages = []
        self.lastmsg = time.perf_counter()

    def send(self, target, msg):
        '''Sends a private message to the target'''
        self.irc.send('PRIVMSG {target} {msg}\n'.encode())

    def pong(self, msg):
        '''Responds to pings sent by the IRC server'''
        self.irc.send(f'PONG {msg[-1]}\n'.encode())
        # So we know it's still connected during debugging
        print('My heart fluttered.')

    def connect(self):
        '''Connects and logs into the IRC server'''
        print(f'connecting to: {self.server}')
        self.irc.connect((self.server, 6667))
        print('connected!')
        self.irc.send(f'USER {self.nick} {self.nick} {self.nick} :Test python irc bot script\n'.encode())
        # Logging in
        self.irc.send(f'PASS {self.passw}\n'.encode())

    def get_text(self):
        '''Recieve, split, and parse data coming from the irc server'''
        messages = []
        data = self.irc.recv(2048)
        if not data:
            self.reconnect()
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
        return parsed[0]

    def close(self):
        '''I guess this is to properly handle closing the connection?'''
        self.irc.close()

    def reconnect(self):
        '''I'm hoping this makes reconnecting easy'''
        print('possible disconnected')
        self.irc.close()
        self.connect()

if __name__ == '__main__':
    '''Example of how the bot class should be used'''
    irc = IRCbot('irc.ppy.sh', 'jamu', 'fd061008')
    irc.connect()
    stayonline = True
    try: # Most of this is to test shutting the bot down
        while stayonline == True:
            for msg in irc.get_text():
                if msg[-1] == '!quit w xd':
                    print('I was told to quit w\nSo I will, bye.')
                    stayonline = False
                    break
                else: print(msg)
        else: irc.close()
    except KeyboardInterrupt:
        irc.close()

# Here's what we recieve after being parsed by the regex:
# Seems 001 is welcome, 375 stars MOTD, 372 is MOTD, and 376 ends MOTD
#     ('cho.ppy.sh', '001', 'Jamu', 'Welcome to the osu!Bancho.\r')
#     ('cho.ppy.sh', '375', 'Jamu', '-\r')
#     ('cho.ppy.sh', '372', 'Jamu', '-                     ______                   __\r')
#     ('cho.ppy.sh', '372', 'Jamu', '-   ____  _______  __/ / __ )____ _____  _____/ /_  ____\r')
#     ('cho.ppy.sh', '372', 'Jamu', '-  / __ \\/ ___/ / / / / __  / __ `/ __ \\/ ___/ __ \\/ __ \\\r')
#     ('cho.ppy.sh', '372', 'Jamu', '- / /_/ (__  ) /_/ /_/ /_/ / /_/ / / / / /__/ / / / /_/ /\r')
#     ('cho.ppy.sh', '372', 'Jamu', '- \\____/____/\\__,_(_)_____/\\__,_/_/ /_/\\___/_/ /_/\\____/\r')
#     ('cho.ppy.sh', '372', 'Jamu', '- osu!bancho (c) ppy Pty Ltd\r')
#     ('cho.ppy.sh', '372', 'Jamu', '- \r')
#     ('cho.ppy.sh', '372', 'Jamu', '-                  .  o ..                  \r')
#     ('cho.ppy.sh', '372', 'Jamu', '-                  o . o o.o                \r')
#     ('cho.ppy.sh', '372', 'Jamu', '-                       ...oo               \r')
#     ('cho.ppy.sh', '372', 'Jamu', '-                         __[]__            \r')
#     ('cho.ppy.sh', '372', 'Jamu', '-                      __|_o_o_o\\__         \r')
#     ('cho.ppy.sh', '372', 'Jamu', '-                      \\'''"/         \r')
#     ('cho.ppy.sh', '372', 'Jamu', '-                       \\. ..  . /          \r')
#     ('cho.ppy.sh', '372', 'Jamu', '-                  ^^^^^^^^^^^^^^^^^^^^\r')
#     ('cho.ppy.sh', '372', 'Jamu', '- \r')
#     ('cho.ppy.sh', '372', 'Jamu', '- web:    https://osu.ppy.sh\r')
#     ('cho.ppy.sh', '372', 'Jamu', '- status: https://twitter.com/osustatus\r')
#     ('cho.ppy.sh', '372', 'Jamu', '- boat:   https://twitter.com/banchoboat\r')
#     ('cho.ppy.sh', '376', 'Jamu', '-\r')
# After repetetive tests 311 seems to be user definitions? 319 seems to be channels the user is in
# 312 seems to be hostnames or something, possibly used to indicate if online in game?
# 318 ends WHOS, obviously, 401 seems to be that the user isn't online, possible need to strip?
#     ('cho.ppy.sh', '311', 'Jamu Tillerino https://osu.ppy.sh/u/2070907 *', 'https://osu.ppy.sh/u/2070907\r                                                                                                                                                                         ')
#     ('cho.ppy.sh', '319', 'Jamu Tillerino', '#osu \r')
#     ('cho.ppy.sh', '312', 'Jamu Tillerino cho.ppy.sh', 'osu!Bancho\r')
#     ('cho.ppy.sh', '318', 'Jamu Tillerino', 'End of /WHOIS list.\r')
#     ('cho.ppy.sh', '401', 'Jamu lksjdfklj', 'No such nick/channel\r')
# I don't think these are much different, but I should look into it
#     ('Jaw--!cho@ppy.sh', 'QUIT', '', 'ping timeout 80s')
#     ('wastingtape!cho@ppy.sh', 'QUIT', '', 'quit')
#     ('ArkaneFenix!cho@ppy.sh', 'QUIT', '', 'replaced (None 5e64f8d1-afee-4bee-afd2-eabdc9fa554e)')
# These are self explanatory, but here for reference of formatting
#     ('Yuuki-chan!cho@ppy.sh', 'PRIVMSG', 'Jamu', 'random')
#     ('Yuuki-chan!cho@ppy.sh', 'PRIVMSG', 'Jamu', '\x01ACTION is listening to [https://osu.ppy.sh/b/1329273 KAMELOT - Liar Liar (Wasteland Monarchy)]\x01')