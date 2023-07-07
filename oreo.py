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

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
