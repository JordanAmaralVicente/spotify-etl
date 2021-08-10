#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3

DATABASE_LOCATION = 'sqlite:///my_played_tracks.sqlite'
USER_ID = 'jordanitalovicente'
TOKEN = 'BQBLdny9iuOzL0ZPZZTZ13SONKcQaQ5S8uAjF0UWZ11EDOlcmNzdWF1_kPry5PoaW1vGl3vmXt-1aZvwqrgU52wIbHyw5DrqT9VnVUrfy-ruYqRU-g_uSiEo2ab1S2jni5qdfxvrKQf1UTcJBmlXI5FzrWyeSplu1it1hwA'

if __name__ == '__main__':
    headers = {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Authorization' : 'Bearer {token}'.format(token=TOKEN),
    }

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    r = requests.get('https://api.spotify.com/v1/me/player/recently-played?after={time}'.format(time=yesterday_unix_timestamp), headers = headers)
    
    data = r.json()

    song_names = []
    artist_names = []
    played_at = []
    timestamps = []

    for song in data['items']:
        song_names.append(song['track']['name'])
        artist_names.append(song['track']['album']['artists'][0]['name'])
        played_at.append(song['played_at'])
        timestamps.append(song['played_at'][0:10])

    song_dict = {
        'song_names': song_names,
        'artist_names': artist_names,
        'played_at': played_at,
        'timestamps': timestamps,
    }

    song_df = pd.DataFrame(song_dict, columns= ['song_names', 'artist_names', 'played_at', 'timestamps'])

    print(song_df)