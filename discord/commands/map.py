from discord.ext import commands

import discord
import asyncio
#import uvloop

#asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

import os, sys, re

sys.path.append(os.path.realpath('../'))

from libs.osuapi  import *
from libs.user    import User
from libs.beatmap import Beatmap
from libs         import pyttanko

class Map:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def map(self, ctx, input=None, mods='nomod'):
        if not input:
            await ctx.send("Please provide a map (link)")
        else:
            oldlink = re.findall('https?://osu.ppy.sh/b/([0-9]*)', input)
            newlink = re.findall('https?://osu.ppy.sh/beatmapsets/[0-9]*\/?\#[a-z]*\/([0-9]*)', input)
            if len(oldlink) > 0: mapid = int(oldlink[0])
            elif len(newlink) > 0: mapid = int(newlink[0])
            else: ctx.send('No proper map link found'); return
            bmdb = Beatmap(mapid)
            bmdb.import_beatmap()
            await self.map_embed(ctx, bmdb, pyttanko.mods_from_str(mods))

    async def map_embed(self, ctx, bmdb, mods):
        # Gets the stars and pp values for the map with the given mods
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
        info += "      ▸ **98%** *{}PP*  **99%** *{}PP*  **100%** *{}PP*\n".format(
            bmdb.PP_98, bmdb.PP_99, bmdb.PP_100)
        em = discord.Embed(description=info, colour=0x00FFC0)
        em.set_author(name=bmdb.artist + ' - ' + bmdb.title + ' by ' + bmdb.creator)
        await ctx.message.channel.send(embed=em)

def mod_emoji(mods):
    """Because emoji >= letters?"""
    mods = mods.replace("EZ", "<:mod_easy:327800791631134731>")
    mods = mods.replace("SD", "<:mod_suddendeath:327800921113231361>")
    mods = mods.replace("SO", "<:mod_spunout:327800910249984001>")
    mods = mods.replace("HR", "<:mod_hardrock:327800817711054858>")
    mods = mods.replace("PF", "<:mod_perfect:327800879019458571>")
    mods = mods.replace("DT", "<:mod_doubletime:327800759741579265>")
    mods = mods.replace("NC", "<:mod_nightcore:327800859989901312>")
    mods = mods.replace("HD", "<:mod_hidden:328172007931904002>")
    mods = mods.replace("FL", "<:mod_flashlight:327800804037885962>")
    mods = mods.replace("RL", "<:mod_relax:327800900318134273>")
    mods = mods.replace("AP", "<:mod_auto:327800780444794880>")
    mods = mods.replace("NF", "<:mod_nofail:327800869523554315>")
    return mods

def setup(bot):
    bot.add_cog(Map(bot))