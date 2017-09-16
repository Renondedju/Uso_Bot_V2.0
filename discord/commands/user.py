from discord.ext import commands
import asyncio
from utils.osuapi import *

class User:
    def __init__(bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def user(ctx, user=None, full=None):
        if user == 'full':
            full = True
            user == 'me'
        if not user:
            user = 'me'
        # Todo check if user has linked their account
        user = 'cookiezi'
        if not full:
            await self.send_user_info(ctx, self.bot.settings['osuApiKey'], user)
        else:
            await self.send_full_info(ctx, self.bot.settings['osuApiKey'], user)

    async def send_user_info(self, ctx, key, user):
        # Todo design embed format
        await self.bot.send_message(ctx.message.channel, "Todo")

    async def send_full_info(self, ctx, key, user):
        # Todo design embed format
        await self.bot.send_message(ctx.message.channel, "Todo")

def setup(bot):
    bot.add_cog(User(bot))