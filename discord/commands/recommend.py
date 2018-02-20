from discord.ext import commands

import discord
import asyncio
#import uvloop

#asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

import os, sys, re

sys.path.append(os.path.realpath('../'))

from libs                import pyttanko
from libs.mods           import *
from libs.user           import User
from libs.osuapi         import *
from libs.preset         import Preset
from libs.beatmap        import Beatmap
from libs.recommendation import REngine

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

            await ctx.send(embed=bmdb.map_embed(mods))

def setup(bot):
    bot.add_cog(Recommendation(bot))