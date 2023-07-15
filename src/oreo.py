from flask import Flask, render_template, request
from twitch import hook_channel as twitch_hook_channel
from webhooks import stream_up
import sys
import json
import requests
import multiprocessing
import sqlite3

CALLBACK = "https://thegreenhouse.dev/oreo"

app = Flask(__name__)
secrets = {}
with open('secrets.json') as f:
    secrets = json.load(f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/oreo/eventstreamup", methods=['POST'])
def event_streamup():
    data = request.json # type: ignore

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

    print(f'telling {{server}} that "{msg}"', file=sys.stdout)
    requests.post(secrets['webhookUrl'], json=discord_message)

@app.route("/oreo/eventstreamdown", methods=['POST'])
def event_streamdown():
    data = request.json # type: ignore
    print(data, file=sys.stdout)
    return '{"msg": "tysm"}'

def watch_channel(username: str, platform: str, message: str, creator: str):
    """
    Will create a webhook for the channel as long as it is supported.
    and store it in the database, then start to watch it.
    This is the top level webhook creation function that the user will interact with
    """

    # do the proper platform specific webhook creation
    platform_id = -1
    if platform == "twitch":
        result = twitch_hook_channel(CALLBACK, username, secrets)
        platform_id = 2
    elif platform == "youtube":
        platform_id = 1
        return { 'error': 'youtube not supported' }
    else:
        return { 'error': f'platform {platform} not supported' }
    
    # check if it worked
    if result['id'] is None:
        print(result, file=sys.stdout)
        return { 'error': 'failed to create webhook' }
    
    # insert into sqlite database
    conn = sqlite3.connect('oreo.sqlite')

    cur = conn.cursor()
    cur.execute('INSERT INTO hooks (channel, platform_id, message, creator) VALUES (?, ?, ?, ?) RETURNING id',
                (username, platform_id, message, creator)
    )

    results = cur.fetchall()

    conn.commit()

    conn.close()

    return { 'id': results[0][0] }

if __name__ == "__main__":
    # simple use, check if it should be running in debug mode
    # using secrets.json is better
    if secrets['ssl']['key'] == '' or secrets['ssl']['crt'] == '':
        app.run(debug=True, host="0.0.0.0", port=8080)
    else:
        # TODO need a better WSGI
        context = (f'/mnt/certs/{secrets["ssl"]["crt"]}', f'/mnt/certs/{secrets["ssl"]["key"]}')
        app.run(debug=False, host="0.0.0.0", port=443, ssl_context=context)
