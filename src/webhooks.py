from twitch import get_auth, get_stream
import sqlite3 # using this because its all i need, and want to try new stuff

def stream_up(data, secrets) -> str:
    channel = data["event"]["broadcaster_user_name"]
    broadcaster_id = data["event"]["broadcaster_user_id"]

    # get the stream info, like title and stuff
    auth = get_auth(secrets['twitch']['client_id'], secrets['twitch']['client_secret'])
    details = get_stream(broadcaster_id, auth['access_token'], secrets['twitch']['client_id']) # type: ignore

    conn = sqlite3.connect('oreo.sqlite')

    cur = conn.cursor()

    cur.execute(f'''
        SELECT hooks.id, channel, message, p.name FROM hooks
            INNER JOIN platforms p on hooks.platform_id = p.id 
            WHERE channel = "{channel}" AND platform_id = 2
    ''') # do i need the name, i know the platform anyway from the call. for later function collection stuff

    # fetch the results
    results = cur.fetchall()

    # send it to each subscription with the proper message
    msg = ""
    id = 0 # should use id and not uuid because uuid would, i think, return every user on every discord to the list
    for row in results:
        id = row[0]
        msg = row[2]
        msg = msg.replace('{channel}', row[1]).replace('{platform}', row[3])
        msg = msg.replace('{link}', f'https://twitch.tv/{channel}')
        msg = msg.replace('{title}', details['title'])
        msg = msg.replace('{game}', details['game_name']) # maybe change to category        

    # close the connection
    conn.close()

    # TODO this only returns the first one, maybe i should do a loop
    return msg, id
