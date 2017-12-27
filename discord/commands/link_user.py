from discord.ext import commands

import json
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
        self.settings = json.loads(open('../config.json', 'r').read())
        self.bot      = bot

    @commands.command(name="link")
    async def _link(self, ctx, *, user=None):
        """ User link command, allows the user
            to link a discord account
            with a osu account """
        if not user:
            await ctx.message.channel.send("Please provide your in game username.")
        else:
            #Everything seems to be good, we can generate a new key

            api_user = get_user(self.settings['osu_api_key'], user, 0)
            if not api_user:
                embed = discord.Embed(title = "Link account", colour = 0xf44242)
                embed.description = "Mhhh, i can't find this user" 
                await ctx.send(embed = embed)
                return

            #Checking if the message comes from a DM or not
            if not isinstance(ctx.message.channel, discord.abc.PrivateChannel):
                embed = discord.Embed(title = "Link account", colour = 0x3498db)
                embed.description = ("Please check your private messages"
                                     "to get your key and the instructions"
                                     "to link your account to uso !")
                await ctx.send(embed = embed)

            #Creating the key
            link = userlink()
            key = link.generate_new_key(api_user[0]['user_id'], ctx.message.author.id)

            #Sending the key to the user
            await ctx.message.author.send("Here is your key : {}".format(key))

def setup(bot):
    bot.add_cog(Link_User(bot))
