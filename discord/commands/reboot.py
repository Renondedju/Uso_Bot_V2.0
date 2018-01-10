from discord.ext import commands

import discord
import asyncio
#import uvloop

#asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

import os # blech

class Reboot:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reboot(self, ctx):
        # Are you cool???
        if ctx.message.author.id self.bot.settings['devs']:
            # Hi cool dude, let me restart for you
            os.system('systemctl restart ircbot')
            os.system('systemctl restart discordbot')
        else: # So you weren't cool after all...
            print('Security! Help!')
