from flask import Flask, render_template, request
import sys
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/eventstreamup", methods=['POST'])
def event_streamup():
    data = request.json # type: ignore
    print(data, file=sys.stdout)

    message = {
        "content": f'{data["event"]["broadcaster_user_name"]} just went live'
    }

    print(message, file=sys.stdout)

    requests.post(webhook_url, json=message)

    return '{"msg": "hello"}'

@app.route("/eventstreamdown", methods=['POST'])
def event_streamdown():
    data = request.json # type: ignore
    print(data, file=sys.stdout)
    return '{"msg": "hello"}'

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
