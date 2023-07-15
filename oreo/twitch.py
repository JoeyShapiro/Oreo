import requests
from webhooks import event_sub

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

def get_channel_id(username: str, bearer_token: str, client_id: str) -> int:
    """
    get the channel id for a given username.
    """
    url = f'https://api.twitch.tv/helix/users?login={username}'
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Client-Id': client_id
    }

    res = requests.get(url, headers=headers)
    return res.json()['data'][0]['id']

def hook_channel(callback: str, username: str, secrets):
    """
    create a webhook for a channel on twitch.tv given the username.
    This will return general information for the user and database.
    """

    auth = get_auth(secrets['twitch']['client_id'], secrets['twitch']['client_secret'])
    broadcaster_id = get_channel_id(username, auth['access_token'], secrets['twitch']['client_id'])

    if broadcaster_id is None:
        return { 'error': 'invalid username' }

    data = event_sub(callback, secrets, broadcaster_id)

    return { 'id': data['data'][0]['id'] }