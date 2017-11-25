from discord.ext import commands

import discord
import asyncio
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

import os, sys

sys.path.append(os.path.realpath('../'))

from libs.osuapi import *
from libs.user import User
from libs.beatmap import Beatmap

class Link_User:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="link")
    async def _link(self, ctx, *, user=None):
        """ Bot command """
        if not user: await ctx.message.channel.send("Please provide your in game username.")
        else: await ctx.message.channel.send("#TODO")

def setup(bot):
    bot.add_cog(Link_User(bot))
