import json
import requests
import time 

Time = time.time()

# Set the webhook_url
webhook_url = ''
slack_data = {
    'embeds' : [
    	{
    		'title' : 'Default embed',
    		'description' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
    		'color': int('0x2ecc71', 16),
    		'author' : {
    			'name' : 'Lorem ipsum',
    			'icon_url' : 'https://cdn.discordapp.com/avatars/213262036069515264/4f4764137e0ff833e6cc93ca152428e4.png'
    		},
    		'footer' : {
    			'text' : 'Lorem ipsum',
    			'icon_url' : 'https://cdn.discordapp.com/avatars/213262036069515264/4f4764137e0ff833e6cc93ca152428e4.png'
    		},
    		'thumbnail' : {
    			'url' : 'https://cdn.discordapp.com/avatars/213262036069515264/4f4764137e0ff833e6cc93ca152428e4.png'
    		},
    		'image' : {
    			'url' : 'https://cdn.discordapp.com/avatars/213262036069515264/4f4764137e0ff833e6cc93ca152428e4.png'
    		},
    		'fields' : [ 
    			{
    				'name' : 'Lorem ipsum',
    				'value' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
    				'inline' : True
    			},
    			{
    				'name' : 'Lorem ipsum',
    				'value' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
    				'inline' : True
    			}
    		]
    	}
    ]
}

response = requests.post(
    webhook_url, data=json.dumps(slack_data),
    headers={'Content-Type': 'application/json'}
)

print ("done in : {}s".format(time.time() - Time))

if response.status_code != 200:
	print ("Status code != 200")