import discord
import asyncio
import time
import sqlite3
import json

bot = commands.Bot(command_prefix='!')
database = sqlite3.connect('UsoDatabase.db')
settings = json.loads(open('config.json', 'r').read())

@bot.command(pass_context=True)
async def ping(ctx):
    t1 = time.perf_counter()
    await bot.send_typing(ctx.message.channel)
    t2 = time.perf_counter()
    await bot.send_message(ctx.message.channel, "Pong. Took {}ms".format(round((t2 - t1) * 100)))

bot.run(settings['discordToken'])