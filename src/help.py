from twitch import hook_channel as twitch_hook_channel
import sys
import json
from twitch import remove_hook

# CALLBACK = 'https://1cd2-2601-243-ce80-5630-8c56-fb84-dadb-fb84.ngrok.io/oreo'
CALLBACK = "https://thegreenhouse.dev/oreo"
log_file = sys.stdout#open('oreo.log', 'a')

secrets = {}
with open('../data/secrets.json') as f:
    secrets = json.load(f)

def watch_channel(username: str, platform: str, message: str, creator: str):
    """
    Will create a webhook for the channel as long as it is supported.
    and store it in the database, then start to watch it.
    This is the top level webhook creation function that the user will interact with
    """

    # do the proper platform specific webhook creation
    platform_id = -1
    if platform == "twitch":
        result = twitch_hook_channel(f'{CALLBACK}/eventstreamup', username, secrets)
        platform_id = 2
    elif platform == "youtube":
        platform_id = 1
        return { 'error': 'youtube not supported' }
    else:
        return { 'error': f'platform {platform} not supported' }
    
    # check if it worked
    if 'id' not in result:
        print(result, file=log_file)
        return { 'error': 'failed to create webhook' }

    return { 'id': -1 }

# watch_channel("yoeyshapiro", "twitch", "{channel} is prolly doing some nerdy stuff on {game} right now. {title} ...i was right. Go check them out at {link}", "yoeyshapiro")

from twitch import get_subs, get_auth
auth = get_auth(secrets['twitch']['client_id'], secrets['twitch']['client_secret'])

# delete all subs
# for sub in get_subs(auth['access_token'], secrets['twitch']['client_id'])['data']:
#     remove_hook(sub['id'], secrets)

print(get_subs(auth['access_token'], secrets['twitch']['client_id']))
