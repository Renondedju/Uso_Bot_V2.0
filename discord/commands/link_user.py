from discord.ext import commands

from __main__ import *

import json
import discord
import asyncio
#import uvloop

#asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

import os, sys

sys.path.append(os.path.realpath('../'))

from libs.osuapi       import *
from libs.user         import User
from libs.beatmap      import Beatmap
from libs.userlink_key import userlink

class Link_User:
    def __init__(self, bot):
        self.settings = settings
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
                                     " to get your key and the instructions"
                                     " to link your account to uso ! *(please"
                                     " make sure that I can send you private messages)*")
                await ctx.send(embed = embed)

            #Creating the key
            link = userlink()
            key  = link.generate_new_key(api_user[0]['user_id'], ctx.message.author.id)

            #Sending the key to the user
            embed = discord.Embed(title = "Link account", colour = 0x3498db)
            embed.description= ("Please open <:osu:310362018773204992> and"
                                " send me __**``{}link {}``**__\nMy ingame name"
                                " is __UsoBot__ -> [profile](https://osu.ppy.sh/u/10406668)"
                                "\nBe careful, this key will __expire in 10 min__".format(self.settings["prefix"], key))
            await ctx.message.author.send(embed=embed)

def setup(bot):
    bot.add_cog(Link_User(bot))
