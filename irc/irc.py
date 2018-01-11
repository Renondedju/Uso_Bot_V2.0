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

    def connect(self, password):
        print(f'connecting to: {self.server}')
        self.irc.connect((self.server, 6667))
        print('connected!')
        self.irc.send(f'USER {self.nick} {self.nick} {self.nick} :Test python irc bot script\n'.encode())
        self.irc.send(f'PASS {password}\n'.encode())
        self.irc.send(f'NICK {self.nick}\n'.encode())

    def get_text(self):
        text = self.irc.recv(2048).decode('utf-8')
        if text.find('PING') != -1:
            print('My heart is fluttering')
            self.irc.send(f'PONG {text.split()[1]}\n'.encode()) 
        return text

if __name__ == '__main__':
    irc = IRCbot('irc.ppy.sh', 'username')
    irc.connect('password')
    while True:
        text = irc.get_text()
        for line in text.split('\n'):
            if line.strip() != '':
                print(line)