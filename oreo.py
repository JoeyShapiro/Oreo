from flask import Flask, render_template, request
import sys
import requests
import sqlite3 # using this because its all i need, and want to try new stuff
import json

app = Flask(__name__)
secrets = {}
with open('secrets.json') as f:
    secrets = json.load(f)
webhook_url = secrets['webhookUrl']

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/eventstreamup", methods=['POST'])
def event_streamup():
    data = request.json # type: ignore

    channel = data["event"]["broadcaster_user_name"]
    conn = sqlite3.connect('oreo.sqlite')

    c = conn.cursor()
    c.execute(f'SELECT channel, message, p.name FROM hooks INNER JOIN platforms p on hooks.platform_id = p.id WHERE channel = "{channel}"')

    # fetch the results
    results = c.fetchall()

    # print the results
    for row in results:
        msg = row[1]
        msg = msg.replace('{channel}', row[0]).replace('{platform}', row[2])
        msg = msg.replace('{link}', f'https://twitch.tv/{channel}')

        discord_message = {
            "content": msg
        }

        print(f'telling {{server}} that "{msg}"')
        requests.post(webhook_url, json=discord_message)

    # close the connection
    conn.close()

    return '{"msg": "hello"}'

@app.route("/eventstreamdown", methods=['POST'])
def event_streamdown():
    data = request.json # type: ignore
    print(data, file=sys.stdout)
    return '{"msg": "hello"}'

def get_auth(client_id: str, client_secret: str):
    url = 'https://id.twitch.tv/oauth2/token'
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": 'client_credentials'
    }
    res = requests.post(url, data)

    return res.json()

def get_stream(broadcaster_id: str, bearer_token: str, client_id: str):
    url = f'https://api.twitch.tv/helix/channels?broadcaster_id={broadcaster_id}'
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Client-Id': client_id
    }

    res = requests.get(url, headers=headers) # must state the headers=
    return res.json()['data'][0] # this is a function, get the only value

if __name__ == "__main__":
    auth = get_auth(secrets['twitch']['client_id'], secrets['twitch']['client_secret'])
    print(auth)
    details = get_stream('141981764', auth['access_token'], secrets['twitch']['client_id']) # type: ignore
    print(details['title'])
    app.run(debug=True, host="0.0.0.0", port=8080)
