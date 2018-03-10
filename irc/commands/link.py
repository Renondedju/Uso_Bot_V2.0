from __main__ import *

from libs.userlink_key import userlink

# link irc command

class irc_command_link:

    def __init__(self, ircbot, user, parameter:str = ""):
        self.bot       = ircbot
        self.user      = user
        self.parameter = parameter
        self.execute()

    def execute(self):
        ''' Execute method '''

        link = userlink()

        if (self.parameter == ""):
            self.bot.send_message(self.user.osu_name, "If you wanna link your discord and osu acount i need a secret code [doc here]")
        else:
            try:
                link.link_account(self.user.osu_id, self.parameter)

                self.bot.send_message(self.user.osu_name, "The link between discord and osu has been done ! Enjoy :)")
            except ValueError:
                
                self.bot.send_message(self.user.osu_name, "The key you send me is invalid or expired, retry the link command on discord !")
            except KeyError:

                self.bot.send_message(self.user.osu_name, "The key you send me doesn't exists, maybe you misstyped ?")
