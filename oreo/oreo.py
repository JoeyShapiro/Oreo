from flask import Flask, render_template, request
from twitch import get_auth, get_stream
from webhooks import stream_up
import sys
import json
import requests
import multiprocessing

app = Flask(__name__)
secrets = {}
with open('secrets.json') as f:
    secrets = json.load(f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/eventstreamup", methods=['POST'])
def event_streamup():
    data = request.json # type: ignore

    # run this in its own thread
    # must pass a deep clone to the process
    process = multiprocessing.Process(target=do_streamup, args=(dict(data),))
    process.start()
    print('started proecc', file=sys.stdout)

    return '{"msg": "tysm"}'

# actually do the stuff
def do_streamup(data):
    msg = stream_up(data, secrets)

    discord_message = {
        "content": msg
    }

    print(f'telling {{server}} that "{msg}"', file=sys.stdout)
    requests.post(secrets['webhookUrl'], json=discord_message)

@app.route("/eventstreamdown", methods=['POST'])
def event_streamdown():
    data = request.json # type: ignore
    print(data, file=sys.stdout)
    return '{"msg": "tysm"}'

if __name__ == "__main__":
    # context = ('server.crt', 'server.key')
    # app.run(debug=True, host="0.0.0.0", port=443, ssl_context=context)
    app.run(debug=True, host="0.0.0.0", port=8080)
