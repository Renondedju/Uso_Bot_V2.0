import os
import json
from pathlib import Path


conf = json.loads(open('../config.json', 'r').read())


BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

DATABASE = 'sqlite:///uso2.db'

MAPS_DIR = BASE_DIR / 'maps'
OSU_API_KEY = conf.get('osu_api_key')
OSU_API_URL = 'https://osu.ppy.sh/api/'
