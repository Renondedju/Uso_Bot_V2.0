from __main__ import *

# Help irc command

class irc_command_help:

    def __init__(self, ircbot, user):
        self.bot  = ircbot
        self.user = user
        self.execute()

    def execute(self):
        ''' Execute method '''
        self.bot.send_message(self.user.osu_name, "Here is all the help ! [{}[wiki]]".format(settings['wiki_link']))