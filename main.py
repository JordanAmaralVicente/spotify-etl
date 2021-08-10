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
TOKEN = 'BQAUE9vGvHHNbUuIonNbmNoVElXya2reuHRQSYyFMPOPvpWXcyy1dmT7ADCAAhHcKrsggE6oCHAGVLxDCIA0nNel6LhZVUaNeUl3yXngNQB56ZB6gK7qJFvxIZmSziwUBT2v900ikYzCwHzpk_xyknMdFmd4EKFjvx2x5jU'

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
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)

    timestamps = df['timestamp'].tolist()
    for timestamp in timestamps:
        if datetime.datetime.strptime(timestamp, '%Y-%m-%d') != yesterday:
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

    if check_if_valid_date(song_df):
        print('Data valid, proceed to load stage')
