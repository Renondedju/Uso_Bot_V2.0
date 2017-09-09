import asyncio
import aiohttp

async def get_beatmap(key, beatmap_id):
    url = "https://osu.ppy.sh/api/get_beatmaps?k={}&b={}".format(key, beatmap_id)
    return await request(url)

async def get_beatmapset(key, set_id):
    url = "https://osu.ppy.sh/api/get_beatmaps?k={}&s={}".format(key, set_id)
    return await request(url)

async def get_scores(key, beatmap_id, user, mode):
    url = "https://osu.ppy.sh/api/get_scores?k={}&u={}&b={}&m={}".format(key, user, beatmap_id, mode)
    return await request(url)

async def get_user(key, user, mode):
    url = "https://osu.ppy.sh/api/get_user?k={}&u={}&m={}".format(key, user, mode)
    return await request(url)

async def get_user_best(key, user, mode, limit):
    url = "https://osu.ppy.sh/api/get_user_best?k={}&u={}&m={}&limit={}".format(key, user, mode, limit)
    return await request(url)

async def get_user_recent(key, user, mode):
    url = "https://osu.ppy.sh/api/get_user_recent?k={}&u={}&m={}".format(key, user, mode)
    return await request(url)

async def request(url):
    async with aiohttp.get(url) as resp:
        return await resp.json()