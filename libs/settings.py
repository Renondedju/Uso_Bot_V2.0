import os
import json
from pathlib import Path


BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__))) / '../'

with open(BASE_DIR / 'config.json', 'r') as config_file:
    conf = json.loads(config_file.read())

DATABASE = 'sqlite:///uso2.db'

MAPS_DIR = BASE_DIR / 'MAPS'
OSU_API_KEY = conf.get('osu_api_key')
OSU_API_URL = 'https://osu.ppy.sh/api/'
