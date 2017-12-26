from discord.ext import commands

import discord
import asyncio
import memcache
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

import os, sys

sys.path.append(os.path.realpath('../'))

from libs.osuapi       import *
from libs.user         import User
from libs.beatmap      import Beatmap
from libs.userlink_key import userlink

class Link_User:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="link")
    async def _link(self, ctx, *, user=None):
        """ User link command, allows the user
            to link a discord account
            with a osu account """
        if not user:
            await ctx.message.channel.send("Please provide your in game username.")
        else:
            #Everything seems to be good, we can generate a new key
            await ctx.message.channel.send("#TODO")

def setup(bot):
    bot.add_cog(Link_User(bot))
