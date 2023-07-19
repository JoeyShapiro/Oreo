from flask import Flask, render_template, request, make_response
from twitch import hook_channel as twitch_hook_channel
from webhooks import stream_up
import sys
import json
import requests
import multiprocessing
import sqlite3

CALLBACK = "https://thegreenhouse.dev/oreo"
log_file = sys.stdout#open('oreo.log', 'a')

app = Flask(__name__)
secrets = {}
with open('../data/secrets.json') as f:
    secrets = json.load(f)

@app.route("/")
def index():
    print(request.json, file=log_file)
    return render_template("index.html")

@app.route("/oreo/eventstreamup", methods=['POST'])
def event_streamup():
    data = request.json # type: ignore

    # fixes an annoying linting null check error
    if data == None:
        data = {}

    # if they send a challenge, has to respond with a challenge
    if request.headers.get('Twitch-Eventsub-Message-Type') == 'webhook_callback_verification':
        resp = event_sub(data)
        return resp

    # run this in its own thread
    # must pass a deep clone to the process
    process = multiprocessing.Process(target=do_streamup, args=(dict(data),))
    process.start()

    return '{"msg": "tysm"}'

# actually do the stuff
def do_streamup(data):
    msg = stream_up(data, secrets)

    discord_message = {
        "content": msg
    }

    print(f'telling {{server}} that "{msg}"', file=log_file)
    requests.post(secrets['webhookUrl'], json=discord_message)

@app.route("/oreo/eventstreamdown", methods=['POST'])
def event_streamdown():
    data = request.json # type: ignore
    print(data, file=log_file)
    return '{"msg": "tysm"}'

# TODO maybe this should also add to database, or verify it
def event_sub(data):
    resp = make_response('')
    resp.headers['Content-Type'] = 'text/plain'

    # check the database for the id
    conn = sqlite3.connect('oreo.sqlite')
    cur = conn.cursor()
    # seems good idea
    cur.execute('SELECT COUNT(*) as count FROM hooks WHERE uuid = ?', (data['challenge'],))
    results = cur.fetchall()

    conn.close()

    # check if i asked for the hook
    if results[0][0] == 0:
        resp.data = 'unrequested hook'
        resp.status_code = 400
    else:
        resp.data = data['challenge']

    print(f'responding to challenge {data}', file=log_file)

    return resp

# TODO move this to another areal. or move api stuff to app.py
# TODO this also needs the hook id, for verification
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
    
    # insert into sqlite database
    conn = sqlite3.connect('oreo.sqlite')

    cur = conn.cursor()
    cur.execute('INSERT INTO hooks (channel, platform_id, message, creator, uuid) VALUES (?, ?, ?, ?, ?) RETURNING id',
                (username, platform_id, message, creator, result['id'])
    )

    results = cur.fetchall()

    conn.commit()

    conn.close()

    return { 'id': results[0][0] }

if __name__ == "__main__":
    # simple use, check if it should be running in debug mode
    # using secrets.json is better
    if sys.argv[1] == "ssl":
        context = (secrets['ssl']['crt'], secrets['ssl']['key'])
        app.run(debug=True, host="0.0.0.0", port=443, ssl_context=context)
    else:
        app.run(debug=True, host="0.0.0.0", port=8080)