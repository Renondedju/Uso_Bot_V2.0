from discord.ext import commands

import discord
import asyncio
#import uvloop

#asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

import os, sys, re

sys.path.append(os.path.realpath('../'))

from libs.osuapi         import *
from libs.user           import User
from libs.beatmap        import Beatmap
from libs.preset         import Preset
from libs.recommendation import REngine
from libs                import pyttanko

class Recommendation:
    def __init__(self, bot):
        self.bot = bot
        self.engine = REngine()

    @commands.command(pass_context=True, aliases=['r'])
    async def recommend(self, ctx, mode='default', power = 1.05):

        user = User(discord_id = ctx.author.id)
        if (user.is_empty()):
            await ctx.send('User not linked')
            return

        preset = Preset(user, mode = mode, power = power)

        if not preset.mode_exists(mode):
            await ctx.send('This preset does not exist !')
            return

        self.engine.recommend(preset, 1)

        for i in range(len(self.engine.recommendatons)):
            bmdb = self.engine.recommendatons[i]
            mods = self.engine.mods[i]

            await self.map_embed(ctx, bmdb, mods, user.osu_name)

    async def map_embed(self, ctx, bmdb, mods, username):
        # Gets the stars and pp values for the map with the given mods
        pyttanko.mods_from_str(mods)
        speed_mult, ar, cs, od, _ = pyttanko.mods_apply(mods, bmdb.diff_approach,
                                                        bmdb.diff_size,
                                                        bmdb.diff_overall)
        info =  "***[Download](https://osu.ppy.sh/d/{})".format(bmdb.beatmap_id)
        info += "([no vid](https://osu.ppy.sh/d/{}n)) ".format(bmdb.beatmap_id)
        info += " [osu!direct](osu://b/{}) ".format(bmdb.beatmapset_id)
        info += "[bloodcat](https://bloodcat.com/osu/s/{})***\n".format(bmdb.beatmap_id)
        info += "  ▸ **Stars:** *{:.2f}★* ".format(bmdb.difficultyrating)
        # This applies any difference to the time with mods
        mins, secs = divmod((bmdb.total_length / speed_mult) / 1000, 60)
        info += "**Length:** *{}:{}*  ".format(int(mins), int(secs))
        info += "**Max Combo:** *{}x*\n    ▸ ".format(bmdb.max_combo)
        if mods != 0: info += " **Mods:** {} ".format(mod_emoji(pyttanko.mods_str(mods)))
        # We only need one or two decimal point precision for these
        info += " **BPM:** *{}*  ".format(round(bmdb.bpm, 2))
        info += "**AR:** *{}*  **CS:** *{}*  **OD:** *{}*\n".format(
            round(ar, 1), round(cs, 1), round(od, 1))
        pp = process_mods(mods, bmdb)
        info += "      ▸ **98%** *{}PP*  **99%** *{}PP*  **100%** *{}PP*\n".format(
            pp['pp_98'], pp['pp_99'], pp['pp_100'])
        em = discord.Embed(description=info, colour=0x00FFC0)
        em.set_author(name=bmdb.artist + ' - ' + bmdb.title + ' by ' + bmdb.creator)
        em.set_footer(text='Recommendation for {}'.format(username))
        await ctx.message.channel.send(embed=em)

def mod_emoji(mods):
    """ Because emoji >= letters? """ # No but carry on :^) -Jamu
    mods = mods.replace("SD", "<:mod_suddendeath:327800921113231361>")
    mods = mods.replace("FL", "<:mod_flashlight:327800804037885962>" )
    mods = mods.replace("DT", "<:mod_doubletime:327800759741579265>" )
    mods = mods.replace("NC", "<:mod_nightcore:327800859989901312>"  )
    mods = mods.replace("HR", "<:mod_hardrock:327800817711054858>"   )
    mods = mods.replace("SO", "<:mod_spunout:327800910249984001>"    )
    mods = mods.replace("PF", "<:mod_perfect:327800879019458571>"    )
    mods = mods.replace("HD", "<:mod_hidden:328172007931904002>"     )
    mods = mods.replace("NF", "<:mod_nofail:327800869523554315>"     )
    mods = mods.replace("RL", "<:mod_relax:327800900318134273>"      )
    mods = mods.replace("EZ", "<:mod_easy:327800791631134731>"       )
    mods = mods.replace("AP", "<:mod_auto:327800780444794880>"       )

    return mods

def process_mods(mods, bmap):
    if mods == '':
        modinfos = {
            'pp_100': bmap.PP_100,
            'pp_99': bmap.PP_99,
            'pp_98': bmap.PP_98,
        }
    else:
        # This should work in theory xd
        modinfo = {
            'pp_100': getattr(bmap, f'PP_100_{mods}'),
            'pp_99': getattr(bmap, f'PP_99_{mods}'),
            'pp_98': getattr(bmap, f'PP_98_{mods}'),
        }
    return modinfos

def setup(bot):
    bot.add_cog(Recommendation(bot))