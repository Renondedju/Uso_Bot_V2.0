from flask import Flask, jsonify, request
from time import perf_counter as time
import sqlite3
import os, sys

sys.path.append(os.path.realpath('../'))

from libs.recommendation import REngine
from libs.user           import User

# The rate tracker, tracks rate per key
class Rates:
    """Allows tracking the request rate for each api key"""
    def __init__(self):
        self.time = time()
        self.checks = {} # An example would be {'key': 5} where 5 is the times this key has made a request
rates = Rates()
limits = {}

# Let's get the engine declared
engine = REngine()

app = Flask(__name__, static_url_path = "")

def parse_params(params):
    """Process the parsed the parameters passed to the api"""
    key = params['k'] if 'k' in params else None
    username = params['u'] if 'u' in params else None
    mods = params['m'] if 'm' in params else ''
    pp = float(params['p']) if 'p' in params and params['p'].replace('.', '', 1).isdigit() else 0
    ranked = not ('r' in params) or ('r' in params and params['r'] == '1')
    return (key, username, mods, pp, ranked)

def check_key(apikey):
    """Checks the provided api key and returns True if valid"""
    if apikey == 'test': return True
    if apikey not in limits:
        database = sqlite3.connect('../UsoDatabase.db')
        cursor = database.cursor()
        cursor.execute("SELECT request_rate FROM users WHERE api_key = ?", [apikey,])
        limits[apikey] = cursor.fetchall()
        database.close()
    if len(limits[apikey]) < 1: # If this is True the key is invalid
        return False
    return True

def limit_check(apikey):
    """This checks if a key has reached it's rate limit"""
    if apikey == 'test': return False
    if rates.time - time() > 60: # Checks if rate limit needs to be reset
        rates.time = time()
        rates.checks = {}
    if apikey not in rates.checks: # Checks if the key has been defined since the last rate reset
        rates.checks[apikey] = 1
        return False
    elif rates.checks[apikey] < limits[apikey][0][0]: # [0][0] is to grab the actual limit for the key since limits[apikey] is [(limit,)]
        rates.checks[apikey] += 1
        return False
    else:
        return True

def build_user(user):
    userinfos = {
        'osu_id': user.osu_id,
        'username': user.osu_name,
        'rank': user.rank,
        'playstyle': user.playstyle,
        'avg_acc': user.accuracy_average,
        'avg_pp': user.pp_average,
        'avg_od': user.od_average,
        'avg_ar': user.ar_average,
        'avg_cs': user.cs_average,
        'avg_bpm': user.bpm_average,
        'low_bpm': user.bpm_low,
        'high_bpm': user.bpm_high,
        'mod_playrates': user.playrate_dict,
    }
    return userinfos

def build_map(engine):
    mapinfos = []
    for i in range(len(engine.recommendatons)):
        bmap = engine.recommendatons[i]
        mods = process_mods(engine.mods[i], bmap)
        mapinfos.append({
            'bmap_id': bmap.beatmap_id,
            'bpm': bmap.bpm,
            'ar': bmap.diff_approach,
            'cs': bmap.diff_size,
            'od': bmap.diff_overall,
            'hp': bmap.diff_drain,
            'stars': bmap.difficultyrating,
            'aim_stars': bmap.aim_stars,
            'speed_stars': bmap.speed_stars,
            'playstyle': bmap.playstyle,
            'length': bmap.total_length,
            'drain_time': bmap.hit_length,
            'max_combo': bmap.max_combo,
            'title': bmap.title,
            'creator': bmap.creator,
            'version': bmap.version,
            'mode': bmap.mode,
            'mods': mods['mods'],
            'pp_100': mods['pp_100'],
            'pp_99': mods['pp_99'],
            'pp_98': mods['pp_98'],
            'pp_97': mods['pp_97']
        })
    return mapinfos

def process_mods(mods, bmap):
    modinfos = {
        'mods': 'nomod', 'pp_100': 0, 
        'pp_99': 0, 'pp_98': 0, 'pp97': 0
    }
    if mods == '':
        modinfos = {
            'mods': 'nomod',
            'pp_100': bmap.PP_100,
            'pp_99': bmap.PP_99,
            'pp_98': bmap.PP_98,
            'pp_97': bmap.PP_97
        }
    if mods == 'HD':
        modinfos = {
            'mods': 'HD',
            'pp_100': bmap.PP_100_HD,
            'pp_99': bmap.PP_99_HD,
            'pp_98': bmap.PP_98_HD,
            'pp_97': bmap.PP_97_HD
        }
    if mods == 'HR':
        modinfos = {
            'mods': 'HR',
            'pp_100': bmap.PP_100_HR,
            'pp_99': bmap.PP_99_HR,
            'pp_98': bmap.PP_98_HR,
            'pp_97': bmap.PP_97_HR
        }
    if mods == 'DT':
        modinfos = {
            'mods': 'DT',
            'pp_100': bmap.PP_100_DT,
            'pp_99': bmap.PP_99_DT,
            'pp_98': bmap.PP_98_DT,
            'pp_97': bmap.PP_97_DT
        }
    if mods == 'DTHD':
        modinfos = {
            'mods': 'HDDT',
            'pp_100': bmap.PP_100_DTHD,
            'pp_99': bmap.PP_99_DTHD,
            'pp_98': bmap.PP_98_DTHD,
            'pp_97': bmap.PP_97_DTHD
        }
    if mods == 'DTHR':
        modinfos = {
            'mods': 'HRDT',
            'pp_100': bmap.PP_100_DTHR,
            'pp_99': bmap.PP_99_DTHR,
            'pp_98': bmap.PP_98_DTHR,
            'pp_97': bmap.PP_97_DTHR
        }
    if mods == 'HRHD':
        modinfos = {
            'mods': 'HDHR',
            'pp_100': bmap.PP_100_HRHD,
            'pp_99': bmap.PP_99_HRHD,
            'pp_98': bmap.PP_98_HRHD,
            'pp_97': bmap.PP_97_HRHD
        }
    if mods == 'DTHRHD':
        modinfos = {
            'mods': 'HDHRDT',
            'pp_100': bmap.PP_100_DTHRHD,
            'pp_99': bmap.PP_99_DTHRHD,
            'pp_98': bmap.PP_98_DTHRHD,
            'pp_97': bmap.PP_97_DTHRHD
        }
    return modinfos

@app.route('/api/<requesttype>', methods = ['GET'])
def get_task(requesttype):
    """Defines the api and what is returned to the end user"""
    if requesttype == 'r':
        key, username, mods, pp, ranked = parse_params(request.args) # Parses the parameters to be used
        if not key or not username: # Handler for when the key or username isn't defined as a parameter
            return jsonify({'error': 'Bad request'})
        if check_key(key) == False: # This checks if the provided key is a valid key
            return jsonify({'error': 'Not a valid api key'})
        if limit_check(key) == False: # This checks if the key hasn't reached it's rate limit
            engine.recommend(User(username), 3) # Self explanatory
            return jsonify({'username': username, 'mods': mods, 'pp': pp, 'ranked': ranked, 'recommended': build_map(engine)})
        else: # This is for when the rate limit has been reached
            return jsonify({'error': 'Rate limit for this key has been reached'})
    elif requesttype == 'user':
        key, username, _, _, _ = parse_params(request.args) # Parses the parameters to be used
        if not key or not username: # Handler for when the key or username isn't defined as a parameter
            return jsonify({'error': 'Bad request'})
        if check_key(key) == False: # This checks if the provided key is a valid key
            return jsonify({'error': 'Not a valid api key'})
        if limit_check(key) == False: # This checks if the key hasn't reached it's rate limit
            return jsonify(build_user(User(username)))
        else: # This is for when the rate limit has been reached
            return jsonify({'error': 'Rate limit for this key has been reached'})
    else: return jsonify({'error': 'Unknown api route'})

# Initializes the flask app if it's run as a script
# Which it should be btw, dunno why it wouldn't
if __name__ == '__main__':
    app.run(debug=True, port=43110)
