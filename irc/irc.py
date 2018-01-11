# -*- coding: utf-8 -*-
import re, os, sys
import socket, time

class IRCbot:
    def __init__(self, server, nick):
        self.server = server
        self.nick = nick
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, target, msg):
        self.irc.send('PRIVMSG {target} {msg}\n'.encode())

    def pong(self, msg):
        self.irc.send(f'PONG {msg[-1]}\n'.encode())
        #print('My heart fluttered.')

    def connect(self, password):
        print(f'connecting to: {self.server}')
        self.irc.connect((self.server, 6667))
        print('connected!')
        self.irc.send(f'USER {self.nick} {self.nick} {self.nick} :Test python irc bot script\n'.encode())
        self.irc.send(f'PASS {password}\n'.encode())
        self.irc.send(f'NICK {self.nick}\n'.encode())

    def get_text(self):
        messages = []
        text = self.irc.recv(2048).decode('utf-8')
        for line in text.split('\n'):
            if line.strip() != '':
                parsed = self.parse_line(line)
                if parsed[1] == 'PING': self.pong(parsed)
                else: messages.append(parsed)
        return messages

    def parse_line(self, line):
        parsed = re.findall('^(?:[:](\S+) )?(\S+)(?: (?!:)(.+?))?(?: [:](.+))?$', line)
        return parsed[0]

    def close(self):
        self.irc.shutdown()
        self.irc.close()

if __name__ == '__main__':
    irc = IRCbot('irc.ppy.sh', 'username')
    irc.connect('password')
    while True:
        messages = irc.get_text()
        for msg in messages:
            print(msg)