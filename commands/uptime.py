from discord.ext import commands
from datetime import datetime, timedelta
import asyncio

class Uptime:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def uptime(self):
        self.bot.say("Bot has been up for " + await time_ago(self.bot.uptime, datetime.now()))

    async def time_ago(time1, time2):
    time_diff = time1 - time2
    timeago = datetime(1,1,1) + time_diff
    time_limit = 0
    time_ago = ""
    if timeago.year-1 != 0:
        time_ago += "**{}** *Year{}* ".format(timeago.year-1, 's' if timeago.year-1 != 1 else '')
        time_limit = time_limit + 1
    if timeago.month-1 !=0:
        time_ago += "**{}** *Month{}* ".format(timeago.month-1, 's' if timeago.month-1 != 1 else '')
        time_limit = time_limit + 1
    if timeago.day-1 !=0 and not time_limit == 3:
        time_ago += "**{}** *Day{}* ".format(timeago.day-1, 's' if timeago.day-1 != 1 else '')
        time_limit = time_limit + 1
    if timeago.hour != 0 and not time_limit == 3:
        time_ago += "**{}** *Hour{}* ".format(timeago.hour, 's' if timeago.hour != 1 else '')
        time_limit = time_limit + 1
    if timeago.minute != 0 and not time_limit == 3:
        time_ago += "**{}** *Minute{}* ".format(timeago.minute, 's' if timeago.minute != 1 else '')
        time_limit = time_limit + 1
    if not time_limit == 3:
        time_ago += "**{}** *Second{}* ".format(timeago.second, 's' if timeago.second != 1 else '')
    return time_ago

def setup(bot):
    bot.add_cog(Uptime(bot))