from __main__ import *

# Test irc command

class irc_command_test:

    def __init__(self, ircbot, user):
        self.bot  = ircbot
        self.user = user
        self.execute()

    def execute(self):
        ''' Execute method '''
        self.bot.send_message(self.user.osu_name, "I'm alive in case of you were wondering")