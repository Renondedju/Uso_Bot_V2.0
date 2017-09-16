from discord.ext import commands
from datetime import datetime
import asyncio, json

bot = commands.Bot(command_prefix='o!', description="Uso! is the best bot")
bot.settings = json_loads(open('config.json', 'r').read())

@bot.event
async def on_ready():
    print('Logged in as {}\nI can see {} users in {} servers'.format(
        bot.user,  len(list(bot.get_all_members())), 
        len(bot.servers)))
    bot.uptime = datetime.now()
    for cog in bot.settings['cogs']:
        try:
            bot.load_extension(cog)
        except Exception as e:
            print('Failed to load cog {}\n{}: {}'.format(cog, type(e).__name__, e))

bot.run(bot.settings['token'])
