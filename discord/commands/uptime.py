from discord.ext import commands
from datetime import datetime, timedelta
import asyncio

class Uptime:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def uptime(self, ctx):
        timeago = datetime(1,1,1) + (self.bot.uptime - datetime.now())
        botuptime = "Bot has been up for "
        if timeago.year-1 != 0:
            botuptime += "{} Year{} ".format(timeago.year-1, 's' if timeago.year-1 != 1 else '')
        if timeago.month-1 !=0:
            botuptime += "{} Month{} ".format(timeago.month-1, 's' if timeago.month-1 != 1 else '')
        if timeago.day-1 !=0:
            botuptime += "{} Day{} ".format(timeago.day-1, 's' if timeago.day-1 != 1 else '')
        if timeago.hour != 0:
            botuptime += "{} Hour{} ".format(timeago.hour, 's' if timeago.hour != 1 else '')
        if timeago.minute != 0:
            botuptime += "{} Minute{} ".format(timeago.minute, 's' if timeago.minute != 1 else '')
        botuptime += "{} Second{}".format(timeago.second, 's' if timeago.second != 1 else '')
        await ctx.message.channel.send(botuptime)

def setup(bot):
    bot.add_cog(Uptime(bot))