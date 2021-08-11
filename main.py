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
TOKEN = 'BQCopOKSWE1iXL4pjZwaPH7n329P0OeqG3ov1jA4_6DQbXjSLf3tHTcEpDNV8rq6m4j874T_9PTHBnDETAev2xSC5OU3A3t3Ewqr9sa7WJTQb6F6HJpQREipUahjckIeUgq43_JvdsJHMQof8fJXLLjGX2I6atvgNk6Y5jY'
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

    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect('my_played_tracks.sqlite')
    cursor = conn.cursor()

    sql_query = '''
    CREATE TABLE IF NOT EXISTS my_played_tracks (
        song_names VARCHAR(200),
        artist_names VARCHAR(200),
        played_at VARCHAR(200),
        timestamp VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
    );
    '''

    cursor.execute(sql_query)
    print('Opened database successfully')

    
    song_df.to_sql('my_played_tracks', con=engine, if_exists='append', index=False)
    
        

    conn.close()
    print('Close database successfully')


