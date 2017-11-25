from discord.ext import commands
from datetime import datetime
import asyncio, json, sys
import logging, traceback
import discord, uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

settings = json.loads(open('../config.json', 'r').read())
bot = commands.Bot(command_prefix=commands.when_mentioned_or(settings['prefix']))
bot.settings = settings

bot.logger = logging.getLogger('usodiscord')
log_format = logging.Formatter(
    '%(asctime)s %(levelname)s %(module)s %(funcName)s %(lineno)d: %(message)s',
    datefmt='[%d/%m/%Y %H:%M]')
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(log_format)
bot.logger.setLevel(logging.WARNING)
bot.logger.addHandler(stdout_handler)

@bot.command(hidden=True)
async def load(ctx, cog):
    '''Loads an extension.'''
    bot.load_extension('commands.' + cog)
    await ctx.message.channel.send('{} loaded.'.format(cog))

@bot.command(hidden=True)
async def unload(ctx, cog):
    '''Unloads an extension.'''
    bot.unload_extension('commands.' + cog)
    await ctx.message.channel.send('{} unloaded.'.format(cog))

@bot.command(hidden=True)
async def reload(ctx, cog):
    '''Reloads an extension.'''
    bot.unload_extension('commands.' + cog)
    bot.load_extension('commands.' + cog)
    await ctx.message.channel.send('{} reloaded.'.format(cog))

@bot.command(hidden=True)
async def ping(ctx):
    await ctx.message.channel.send('{:.2f}ms'.format(bot.latency * 1000))

bot.remove_command('help')
@bot.command(name='help')
async def _help(ctx):
    await ctx.message.channel.send('Google it :V')

@bot.event
async def on_command_error(ctx, error):
    errormsg  = '```In {}:\n'.format(ctx.command.qualified_name)
    errormsg += '{}: {}```\n'.format(error.original.__class__.__name__, error.original)
    errormsg += 'Ask about it here for more information: https://discord.gg/Qsw3yD5'
    await ctx.message.channel.send(errormsg)
    bot.logger.exception(type(error).__name__, exc_info=error)

#@bot.event
#async def on_guild_create(guild):
#     await dblpost()
#
#@bot.event
#async def on_guild_remove(guild):
#     await dblpost()
#
#async def dblpost():
#    headers = {'Authorization': bot.settings['dbltoken']}
#    data = {'server_count': len(bot.guilds)}
#    async with aiohttp.ClientSession() as session:
#        req = await session.post('https://discordbots.org/api/bots/{}/stats'.format(bot.user.id), data=data, headers=headers)

@bot.event
async def on_ready():
    print('Logged in as {}\nI can see {} users in {} servers'.format(
        bot.user,  len(list(bot.get_all_members())),
        len(bot.guilds)))
    bot.uptime = datetime.now()
    for cog in bot.settings['cogs']:
        try: bot.load_extension(cog)
        except: bot.logger.exception(sys.exc_info())

bot.run(bot.settings['discord_token'])
