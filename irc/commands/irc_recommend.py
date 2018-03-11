from __main__ import *

from libs.mods           import *
from libs.user           import User
from libs.preset         import Preset
from libs.beatmap        import Beatmap
from libs.recommendation import REngine

# r irc command

class irc_command_recommend:

    def __init__(self, ircbot, user, parameters:str):
        self.bot        = ircbot
        self.user       = user
        self.parameters = parameters
        self.engine     = REngine()
        self.execute()

    def execute(self):
        ''' Execute method '''

        mode  = 'default'
        power = 1.05

        if (self.parameters != ""):
            mode = self.parameters

        preset = Preset(self.user, mode = mode.lower(), power = power)

        if not preset.mode_exists(mode):
            self.bot.send_message(self.user.osu_name, "This preset doesn't exists sorry :)")
            return

        self.engine.recommend(preset, 1)

        for i in range(len(self.engine.recommendatons)):
            bmdb = self.engine.recommendatons[i]
            mods = self.engine.mods[i]

            download_link = "[https://osu.ppy.sh/beatmapsets/{0}#osu/{1}[{2} : {3}]]".format(
                bmdb.beatmapset_id, bmdb.beatmap_id, bmdb.title, bmdb.version)

            diff  = "CS{} AR{} OD{} ♫ Bmp {}".format(bmdb.diff_size, bmdb.diff_approach, bmdb.diff_overall, bmdb.bpm)
            pps   = "97%: {}pp, 98%: {}pp, 100%: {}pp".format(
                getattr(bmdb, 'PP_97'  + mods),
                getattr(bmdb, 'PP_98'  + mods),
                getattr(bmdb, 'PP_100' + mods))

            mods = mods.strip('_')

            reply = "{0}   | {4} | {3} - {1} (using {2} preset)".format(download_link, mods, preset.name, diff, pps)

            self.bot.send_message(self.user.osu_name, reply)