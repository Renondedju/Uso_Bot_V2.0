# -*- coding: utf-8 -*-

import sys
import socket
import requests
import json

settings = json.loads(open('../config.json', 'r').read())
irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

username = settings['IRCname']
password = settings['IRCtoken']
RunDiscord = True

print("\nConnecting to irc.ppy.sh:6667")
irc_socket.connect(("irc.ppy.sh", 6667))

irc_socket.send(bytes("PASS " + password + "\n", "UTF-8"))
irc_socket.send(bytes("NICK " + username + "\n", "UTF-8"))
irc_socket.send(bytes("USER " + username + " " + username + " " + username + " " + username + "\n", "UTF-8"))

irc_msg = irc_socket.recv(2048).decode("UTF-8")
irc_msg = irc_msg.strip('\n\r').split("\r\n")

for msg in irc_msg:
	if("464" in msg):
		print("Bad Authorization. Please check your login details")
		sys.exit(0)

print("Connected...\n")

irc_socket.send(bytes("PRIVMSG Renondedju :Connected to bancho !\n", "UTF-8"))
irc_socket.send(bytes("JOIN #osu\n", "UTF-8"))

running = True
while running:
	irc_messages = irc_socket.recv(2048).decode("UTF-8")
	irc_messages = irc_messages.strip('\r\n').split("\n")

	for irc_msg in irc_messages:
		if ("PRIVMSG" in irc_msg):

			sender_name = irc_msg.split('!', 1)[0][1:]
			sender_message = irc_msg.split('PRIVMSG', 1)[1].split(':', 1)[1]
			private = not "cho@ppy.sh PRIVMSG #osu" in irc_msg.split("!", 1)[1]

			if private:
				print (sender_name + ": " + sender_message)

		if ("PING" in irc_msg):
			sender_message = irc_msg.split(' ')[1]
			irc_socket.send(bytes("PONG " + sender_message + "\n", "UTF-8"))
			print ('\x1b[1;32;40m' + "PONG " + sender_message + '\x1b[0m')