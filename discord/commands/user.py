from discord.ext import commands

import discord
import asyncio
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

import os, sys

sys.path.append(os.path.realpath('../'))

from libs.osuapi import *
from libs.user import User
from libs.beatmap import Beatmap

class _User:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def user(self, ctx, *, user=None):
        """ Bot command """
        if not user:
            user = 'cookiezi'

        # Todo check if user has linked their account
        user = get_user(self.bot.settings['osu_api_key'], user, 0)[0]
        levelint, levelpercent = divmod(float(user['level']), 1)

        # Creating the main infos displays
        info =  "▸ Global Rank:    #{} ({}#{})\n".format(
            user['pp_rank'],
            user['country'],
            user['pp_country_rank'])

        info += "▸ Level:          {} ({:.2f}%)\n".format(levelint, levelpercent * 100)
        info += "▸ Total PP:       {:.2f}\n".format(float(user['pp_raw']))
        info += "▸ Hit Accuracy:   {:.2f}%\n".format(float(user['accuracy']))
        info += "▸ Playcount:      {:,}\n".format(int(user['playcount']))
        info += "▸ Ranked Score:   {:,}\n".format(int(user['ranked_score']))
        info += "▸ Total Score:    {:,}\n\n".format(int(user['total_score']))
        info += "▸ Hits:               (300/100/50)\n"

        totalhits = int(user['count300']) + int(user['count100']) + int(user['count50'])

        #300/100/50
        n300 = "{}".format(int(user['count300']))
        n100 = "{}".format(int(user['count100']))
        n50  = "{}".format(int(user['count50']))

        # 300%/100%/50% 
        p300 = "{:.2f}%".format(int(user['count300']) / totalhits * 100)
        p100 = "{:.2f}%".format(int(user['count100']) / totalhits * 100)
        p50  = "{:.2f}%".format(int(user['count50'])  / totalhits * 100)

        info += "{:>35}".format("{}//{}//{}\n".format(n300, n100, n50))
        info += "{:>35}".format("{}{}//{}{}//{}{}\n".format(' ' * (len(n300) - len(p300)),
                                                      p300, ' ' * (len(n100) - len(p100)),
                                                      p100, ' ' * (len(n50)  - len(p50)),
                                                      p50))
        # Ranks 
        info += "▸ Ranks:                  (SS/S/A)\n"
        info += "{:>35}".format("{}//{}//{}\n".format(
            int(user['count_rank_ss']),
            int(user['count_rank_s']),
            int(user['count_rank_a'])))

        # Creating the container (embed)
        em = discord.Embed(description="```Prolog\n" + info + "\n```", color=0x00FFC0)

        em.set_author(
            name="Profile for {}".format(user['username']),
            icon_url='https://osu.ppy.sh/images/flags/{}.png'.format(user['country']),
            url='https://osu.ppy.sh/u/{}'.format(user['user_id']))

        em.set_thumbnail(url='https://a.ppy.sh/{}'.format(user['user_id']))

        await ctx.message.channel.send(embed=em)

def setup(bot):
    bot.add_cog(_User(bot))
