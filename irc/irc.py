# -*- coding: utf-8 -*-
import re, os, sys
import socket, time

class IRCbot:
    def __init__(self, server, nick, passw):
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.nick = nick
        self.passw = passw
        self.buffer = {}

    def send_message(self, target, msg):
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

    def check_buffer(self): # Is there a way to compress these two into one function, since they're mostly the same?
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
        self.irc.send(f'PRIVMSG {target} {msg}\n'.encode())
        print(f'To {target}: {msg}') # So we can see the messages sent

    def pong(self, msg):
        '''Responds to pings sent by the IRC server'''
        self.irc.send(f'PONG {msg[-1]}\n'.encode())
        # So we know it's still connected during debugging
        print('My heart fluttered.')

    def connect(self):
        '''Connects and logs into the IRC server'''
        self.irc.connect((self.server, 6667))
        print(f'Connected to: {self.server}')
        self.irc.send(f'USER {self.nick} {self.nick} {self.nick} :Test bot\n'.encode())
        self.irc.send(f'PASS {self.passw}\n'.encode())
        self.irc.send(f'NICK {self.nick}\n'.encode())

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
        try: return parsed[0] # Don't judge this, I just want to see why it randomly crashes sometimes xd
        except: print(line); return ('', '', '', '')

    def close(self):
        '''I guess this is to properly handle closing the connection?'''
        self.irc.close()

    def reconnect(self):
        '''I'm hoping this makes reconnecting easy'''
        print('Reconnecting...')
        self.irc.close()
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

if __name__ == '__main__':
    '''Example of how the bot class should be used'''
    irc = IRCbot('irc.ppy.sh', 'username', 'password')
    irc.connect()
    stayonline = True
    try: # Might add certain handlers for these in the future
        while stayonline == True:
            for msg in irc.get_text():
                if msg[1] == 'PRIVMSG':
                    sender = msg[0].split('!')[0]
                    print(f'From {sender}: {msg[3]}')
                    if msg[3] == 'test':
                        irc.send_message(sender, 'you failed')
                    elif msg[3] == 'test me':
                        irc.send_message(sender, '\x01ACTION is a cool bot\x01')
                    elif msg[3] == 'test link':
                        irc.send_message(sender, '[https://osu.ppy.sh/home Here]\'s a good time')
                elif msg[1] in ['001', '372', '375', '376']:
                    print(msg[3].strip())
                elif msg[1] in ['311', '319', '312', '318', '401']:
                    print(f'Whois {msg[2].split(" ")[1]}: {msg[3].strip()}')
                elif msg[1] == '464':
                    print('Bad authentication token.')
                    stayonline = False
                    break
                else: print(msg)
            irc.check_buffer()
        else: irc.close()
    except KeyboardInterrupt:
        irc.close()
