#Starting script
#Killing any old tasks
echo -e 'Killing old tasks ...'
pkill -f discord.py
pkill -f irc_socket.py
#Restarting scripts
echo -e 'Restarting scripts ...'
python3.5 discord/discord.py &
python3.5 irc/irc_socket.py &
