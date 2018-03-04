from __main__ import *

from discord.ext import commands
from datetime    import datetime

import sys
import json
import discord
import asyncio
import logging
import traceback

import os, sys

sys.path.append(os.path.realpath('../'))

from libs.logs import Log
from libs.user import User

bot          = commands.Bot(command_prefix=commands.when_mentioned_or(settings['prefix']))
bot.settings = settings

bot.logger = logging.getLogger('usodiscord')
log_format = logging.Formatter(
    '%(asctime)s %(levelname)s %(module)s %(funcName)s %(lineno)d: %(message)s',
    datefmt='[%d/%m/%Y %H:%M]')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(log_format)

bot.logger.setLevel  (logging.WARNING)
bot.logger.addHandler(stdout_handler)

# Load command
@bot.command(hidden=True)
async def load(ctx, cog):
    """Loads an extension."""
    bot.load_extension('commands.' + cog)
    await ctx.send('{} loaded.'.format(cog))

# Unload command
@bot.command(hidden=True)
async def unload(ctx, cog):
    '''Unloads an extension.'''
    bot.unload_extension('commands.' + cog)
    await ctx.send('{} unloaded.'.format(cog))

# Reload command
@bot.command(hidden=True)
async def reload(ctx, cog):
    '''Reloads an extension.'''
    bot.unload_extension('commands.' + cog)
    bot.load_extension('commands.' + cog)
    await ctx.send('{} reloaded.'.format(cog))

# Ping command
@bot.command(hidden=True)
async def ping(ctx):
    await ctx.send('{:.2f}ms'.format(bot.latency * 1000))

# Help command
bot.remove_command('help')
@bot.command(name='help')
async def _help(ctx):
    await ctx.send('https://github.com/Renondedju/Uso_Bot_V2.0/blob/master/docs/index.md')

# --- BOT CHECKS ---

@bot.check
async def command_check(ctx):
    """ Creating logs for each command """
    user = User(0)
    user.set_logs_infos(ctx.message.author.name,
                        ctx.message.author.avatar,
                        ctx.message.author.id)
    logs.add_log(user, ctx.guild.name + '/' + str(ctx.message.channel) + ' : ' + ctx.message.content)
    return True

# --- BOT EVENTS ---

#On command error
@bot.event
async def on_command_error(ctx, error):
    if (ctx.command):
        errors = traceback.format_exception(type(error), error, error.__traceback__)
        output = ''
        for line in errors:
            output += line

        user = User(0)
        user.set_logs_infos(ctx.message.author.name,
                            ctx.message.author.avatar,
                            ctx.message.author.id)
        logs.add_error_log(user, 'On command {}'.format(ctx.command.qualified_name), output)
        logs.send_logs()

        await ctx.send('Crap, an error ! Need some healing ? {}'.format(settings['discord_server']))
        bot.logger.exception(type(error).__name__, exc_info=error)

# On guild create
@bot.event
async def on_guild_create(guild):
    logs.add_server_log('added', guild)
    logs.send_logs()
    await dblpost()

#TODO test thoses logs (discord v1.0.0)

#On guild remove
@bot.event
async def on_guild_remove(guild):
    logs.add_server_log('removed', guild)
    logs.send_logs()
    await dblpost()

#Discord bot list api update
async def dblpost():
   headers = {'Authorization': bot.settings['dbltoken']}
   data = {'server_count': len(bot.guilds)}
   async with aiohttp.ClientSession() as session:
       req = await session.post('https://discordbots.org/api/bots/{}/stats'.format(bot.user.id), data=data, headers=headers)

# On ready
@bot.event
async def on_ready():
    logs.add_warning_log('Logged in as {}\nI can see {} users in {} servers'.format(
        bot.user.mention,  len(list(bot.get_all_members())),
        len(bot.guilds)))
    logs.send_logs()

    bot.uptime = datetime.now()
    for cog in bot.settings['cogs']:
        try:
            bot.load_extension(cog)
            print ("Loaded : ", end='')
            print (cog)
        except:
            bot.logger.exception(sys.exc_info())
            print ("Failed to load : ", end='')
            print (cog)
    print ("Ready !")

# Running the bot
def run_discord():
    bot.run(bot.settings['discord_token'])

    logs.add_warning_log('Logged out !')
    logs.send_logs()

    print('Uso discord exited')