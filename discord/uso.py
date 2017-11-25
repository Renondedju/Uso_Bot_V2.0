from discord.ext import commands
from datetime    import datetime

import asyncio, json, sys
import logging, traceback
import discord, uvloop

import os, sys

sys.path.append(os.path.realpath('../'))

from libs.logs import Log
from libs.user import User

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

settings     = json.loads(open('../config.json', 'r').read())
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

logs = Log()

# Load command
@bot.command(hidden=True)
async def load(ctx, cog):
    '''Loads an extension.'''
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
    await ctx.send('Google it :V')

# --- BOT CHECKS ---

@bot.check
async def command_check(ctx):
    user = User(0)
    user.set_logs_infos(ctx.message.author.name,
                        ctx.message.author.avatar,
                        ctx.message.author.id)
    logs.add_log(user, ctx.message.content)
    logs.send_logs()
    return True

# --- BOT EVENTS ---

#On command error
@bot.event
async def on_command_error(ctx, error):
    logs.add_error_log()
    if (ctx.command):
        errormsg  = '```n {}:\n'.format(ctx.command.qualified_name)
        errormsg += '{}: {}```\n'.format(error.original.__class__.__name__, error.original)
        errormsg += 'Ask about it here for more information: https://discord.gg/Qsw3yD5'
        await ctx.send(errormsg)
        bot.logger.exception(type(error).__name__, exc_info=error)

# On guild create
@bot.event
async def on_guild_create(guild):
    logs.add_server_log('added', guild)
    await dblpost()

#TODO test thoses logs (discord v1.0.0)

#On guild remove
@bot.event
async def on_guild_remove(guild):
    logs.add_server_log('removed', guild)
    await dblpost()

async def dblpost():
   headers = {'Authorization': bot.settings['dbltoken']}
   data = {'server_count': len(bot.guilds)}
   async with aiohttp.ClientSession() as session:
       req = await session.post('https://discordbots.org/api/bots/{}/stats'.format(bot.user.id), data=data, headers=headers)

# On ready
@bot.event
async def on_ready():
    print('\nLogged in as {}\nI can see {} users in {} servers'.format(
        bot.user,  len(list(bot.get_all_members())),
        len(bot.guilds)))

    bot.uptime = datetime.now()
    for cog in bot.settings['cogs']:
        try: bot.load_extension(cog)
        except: bot.logger.exception(sys.exc_info())

# Running the bot
bot.run(bot.settings['discord_token'])
