#!/bin/sh
#Starting script

python_env=python3

#Killing any old tasks

echo -e 'Killing old tasks ...'
pkill -f uso.py
pkill -f irc_socket.py

#Restarting scripts
echo -e 'Restarting scripts ...'
$python_env discord/uso.py &
#$python_env irc/irc_socket.py &