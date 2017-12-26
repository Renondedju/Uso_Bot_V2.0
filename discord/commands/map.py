from discord.ext import commands

import discord
import asyncio
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

import os, sys

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
            mapid = input.replace('https://osu.ppy.sh/b/', '').split('?')[0]
            bmdb = Beatmap(mapid)
            bmap = pyttanko.parser().map(open(bmdb.beatmaps_path + mapid + '.osu'))
            await self.map_embed(ctx, bmdb, bmap, pyttanko.mods_from_str(mods.lower()))

    async def map_embed(self, ctx, bmdb, bmap, mods):
        # Gets the stars and pp values for the map with the given mods
        stars = pyttanko.diff_calc().calc(bmap, mods=mods)
        pp100, pp99, pp98 = await self.get_pp_by_acc(bmap, stars, mods)
        speed_mult, ar, cs, od, _ = pyttanko.mods_apply(mods, bmdb.diff_approach, 
                                                        bmdb.diff_size, 
                                                        bmdb.diff_overall)
        info =  "***[Download](https://osu.ppy.sh/d/{})".format(bmdb.beatmap_id)
        info += "([no vid](https://osu.ppy.sh/d/{}n)) ".format(bmdb.beatmap_id)
        info += " [osu!direct](osu://b/{}) ".format(bmdb.beatmapset_id)
        info += "[bloodcat](https://bloodcat.com/osu/s/{})***\n".format(bmdb.beatmap_id)
        info += "  ▸ **Stars:** *{:.2f}★* ".format(stars.total)
        # This applies any difference to the time with mods
        mins, secs = divmod((bmap.hitobjects[-1].time / speed_mult) / 1000, 60)
        info += "**Length:** *{}:{}*  ".format(int(mins), int(secs))
        info += "**Max Combo:** *{}x*\n    ▸ ".format(bmdb.max_combo)
        if mods != 0: info += " **Mods:** {} ".format(mod_emoji(pyttanko.mods_str(mods)))
        # We only need one or two decimal point precision for these
        info += " **BPM:** *{}*  ".format(round(bmdb.bpm, 2))
        info += "**AR:** *{}*  **CS:** *{}*  **OD:** *{}*\n".format(
            round(ar, 1), round(cs, 1), round(od, 1))
        info += "      ▸ **98%** *{}PP*  **99%** *{}PP*  **100%** *{}PP*\n".format(
            pp98, pp99, pp100)
        em = discord.Embed(description=info, colour=0x00FFC0)
        em.set_author(name=bmdb.artist + ' - ' + bmdb.title + ' by ' + bmdb.creator)
        await ctx.message.channel.send(embed=em)

    async def get_pp_by_acc(self, bmap, stars, mods):
        """Uses pyttanko to get the pp for 98%, 99% and 100% accs"""
        n300, n100, n50 = pyttanko.acc_round(100, len(bmap.hitobjects), 0)
        pp100, _, _, _, _ = pyttanko.ppv2(stars.aim, stars.speed, bmap=bmap, mods=mods, n300=n300, n100=n100, n50=n50, nmiss=0)
        n300, n100, n50 = pyttanko.acc_round(99, len(bmap.hitobjects), 0)
        pp99, _, _, _, _ = pyttanko.ppv2(stars.aim, stars.speed, bmap=bmap, mods=mods, n300=n300, n100=n100, n50=n50, nmiss=0)
        n300, n100, n50 = pyttanko.acc_round(98, len(bmap.hitobjects), 0)
        pp98, _, _, _, _ = pyttanko.ppv2(stars.aim, stars.speed, bmap=bmap, mods=mods, n300=n300, n100=n100, n50=n50, nmiss=0)
        return (int(pp100), int(pp99), int(pp98))

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