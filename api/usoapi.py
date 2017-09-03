from flask import Flask, jsonify
from datetime import datetime, timedelta
from urllib.parse import parse_qs
import sqlite3

# The rate tracker, tracks rate per key
class Rates:
    """Allows tracking the request rate for each api key"""
    def __init__(self):
        self.time = datetime.now()
        self.checks = {} # An example would be {'key': 5} where 5 is the times this key has made a request
rates = Rates()
limits = {}

app = Flask(__name__, static_url_path = "")

def parse_params(parameters):
    """Process the parsed the parameters passed to the api"""
    params = parse_qs(parameters)
    key = params['k'][0] if 'k' in params else None
    username = params['u'][0] if 'u' in params else None
    mods = params['m'][0] if 'm' in params else ''
    pp = float(params['p'][0]) if 'p' in params and params['p'][0].replace('.', '', 1).isdigit() else 0
    ranked = not ('r' in params) or ('r' in params and params['r'][0] == '1')
    return (key, username, mods, pp, ranked)

def check_key(apikey):
    """Checks the provided api key and returns True if valid"""
    if apikey not in limits:
        database = sqlite3.connect('UsoDatabase.db')
        cursor = database.cursor()
        cursor.execute("SELECT request_rate FROM users WHERE api_key = ?", [apikey,])
        limits[apikey] = cursor.fetchall()
        database.close()
    if len(limits[apikey]) < 1: # If this is True the key is invalid
        return False
    return True

def limit_check(apikey):
    """This checks if a key has reached it's rate limit"""
    if rates.time < datetime.now() - timedelta(seconds=60): # Checks if rate limit needs to be reset
        rates.time = datetime.now()
        rates.checks = {}
    if apikey not in rates.checks: # Checks if the key has been defined since the last rate reset
        rates.checks[apikey] = 1
        return False
    elif rates.checks[apikey] < limits[apikey][0][0]: # [0][0] is to grab the actual limit for the key since limits[apikey] is [(limit,)]
        rates.checks[apikey] += 1
        return False
    else:
        return True

@app.route('/api/<parameters>', methods = ['GET'])
def get_task(parameters):
    """Defines the api and what is returned to the end user"""
    key, username, mods, pp, ranked = parse_params(parameters) # Parses the parameters to be used
    recommended = ['#TODO'] # Self explanatory
    if not key or not username: # Handler for when the key or username isn't defined as a parameter
        return make_response(jsonify({'error': 'Bad request'}))
    if check_key(key) == False: # This checks if the provided key is a valid key
        return jsonify({'error': 'Not a valid api key'})
    if limit_check(key) == False: # This checks if the key hasn't reached it's rate limit
        return jsonify({'key': key, 'username': username, 'mods': mods, 'pp': pp, 'ranked': ranked, 'recommended': recommended})
    else: # This is for when the rate limit has been reached
        return jsonify({'error': 'Rate limit for this key has been reached'})

# Initializes the flask app if it's run as a script
if __name__ == '__main__':
    app.run(debug = True)
