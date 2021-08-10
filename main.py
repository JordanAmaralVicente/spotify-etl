#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
import datetime
import sqlite3
import time

DATABASE_LOCATION = 'sqlite:///my_played_tracks.sqlite'
USER_ID = 'jordanitalovicente'
TOKEN = 'BQBOfi58nLwH7n7QggfDFvol8pIMatq4pwAgWABcp_bjibO1Mqbs5U2sRTx_4EyFfgG50fFmS8Dbw10998WOv6JOu3iJcv6WPjNUL30prDpHv2jr0zA2mjw5sXCpgzk3HsDEGQG_pI_1H7Qx_5Flf5dDa4k0_iglWzhdRzA'
def check_if_valid_date(df: pd.DataFrame) -> bool:
    if df.empty:
        print('No songs downloaded. Finishing execution.')
        return False

    if pd.Series(df['played_at']).is_unique:
        pass
    else:
        raise Exception('Primary Key Check is violated')

    if df.isnull().values.any():
        raise Exception('Null value found')

    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp())

    timestamps = df['played_at'].tolist()
    for timestamp in timestamps:
        datetimeObj = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
        timestamp = time.mktime(datetimeObj.timetuple())
        if timestamp < yesterday_unix_timestamp:
            raise Exception('At least one of the returned songs does not come from within the last 24 hours')

    return True


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
    timestamp = []

    for song in data['items']:
        song_names.append(song['track']['name'])
        artist_names.append(song['track']['album']['artists'][0]['name'])
        played_at.append(song['played_at'])
        timestamp.append(song['played_at'][0:10])

    song_dict = {
        'song_names': song_names,
        'artist_names': artist_names,
        'played_at': played_at,
        'timestamp': timestamp,
    }

    song_df = pd.DataFrame(song_dict, columns= ['song_names', 'artist_names', 'played_at', 'timestamp'])

    print(song_df)
    if check_if_valid_date(song_df):
        print('Data valid, proceed to load stage')
