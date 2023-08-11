import sqlite3

"""
INSERT INTO followers (username, hook_id)
    VALUES ('yoeyshapiro',
            (
                SELECT hooks.id FROM hooks
                    inner join platforms p on hooks.platform_id = p.id
                    WHERE p.name = 'twitch' AND channel = 'yoeyshapiro' AND hoook_type = 'streamup'
            )
        )
"""
def follow_channel_hook(username: str, channel: str, platform: str, hook_type: str):
    """
    alllow a user to get notified when a hook they follow is posted
    """

    conn = sqlite3.connect('oreo.sqlite')
    cur = conn.cursor()

    # get the hook id
    # this way is cleaner than sub queries
    cur.execute('''
                SELECT hooks.id FROM hooks 
                    INNER JOIN platforms p ON hooks.platform_id = p.id 
                    WHERE p.name = ? AND channel = ? AND hoook_type = ?
                '''
                , platform, channel, hook_type)
    results = cur.fetchall()

    # insert into followers table
    cur.execute('INSERT INTO followers (username, hook_id) VALUES (?, ?)', username, results[0][0])
    cur.fetchall()
    cur.commit()

    conn.close()
