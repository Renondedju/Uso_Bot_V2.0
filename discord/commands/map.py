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
    async def map(self, ctx, input=None, mods=''):
        
        if not input:
            await ctx.send("Please provide a map (link)")
        
        else:
            oldlink = re.findall('https?://osu.ppy.sh/b/([0-9]*)', input) #should be obsolete soon
            newlink = re.findall('https?://osu.ppy.sh/beatmapsets/[0-9]*\/?\#[a-z]*\/([0-9]*)', input)
            
            if len(oldlink) > 0: 
                mapid = int(oldlink[0])
            elif len(newlink) > 0: 
                mapid = int(newlink[0])
            else: 
                ctx.send('No proper map link found')
                return

            bmdb = Beatmap(mapid)

            await ctx.send(embed=bmdb.map_embed(mods))



def setup(bot):
    bot.add_cog(Map(bot))