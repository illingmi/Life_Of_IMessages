import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from matplotlib import style
from collections import Counter
import os
import sys
import json
import spotipy
import webbrowser
import time
import datetime
import spotipy.util as util
from json.decoder import JSONDecodeError

# Get the username and playlist id from terminal
username = sys.argv[1]
playlist_id = sys.argv[2]
scope = 'user-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private'

# USER ID: 	mibaeoch3ierdvfq3g2wdvvl5
# PLAYLIST ID: 6RRGjdDeTm9tBI1nwkVzBE

# USER AUTHENTICATION COMMANDS:
    # $env:SPOTIPY_CLIENT_ID="a8fd8489dea042b9b5b705907665e75b"
    # $env:SPOTIPY_CLIENT_SECRET="4f2b0aef10054fc18f2a3711b9d8c14b"
    # $env:SPOTIPY_REDIRECT_URI="http://google.ca/"

# Erase cache and prompt for user permission
try:
    token = util.prompt_for_user_token(username, scope)
except:
    os.remove(f".cache-{username}")
    # os.remove('.cache-{}'.format(username))
    token = util.prompt_for_user_token(username, scope)

# Create our spotifyObject
spotifyObject = spotipy.Spotify(auth=token)
user = spotifyObject.current_user()

# Set Up File
orgFile = pd.read_csv('A_messages.csv')
keep_col = ['Message Date','Type', 'Sender Name', 'Text']
df = orgFile[keep_col]

# Datetime stuff
df['datetime'] = pd.to_datetime(df['Message Date'], infer_datetime_format=True)
df['datetime'].dtype

# Get list of spotify songs
dfSpotify = df[df['Text'].str.contains("open.spotify", case=False) == True].sort_values(by='datetime')
dfAppleMusic = df[df['Text'].str.contains("itunes.apple", case=False) == True].sort_values(by='datetime')
print(dfAppleMusic)

dfAlbums = dfSpotify[dfSpotify['Text'].str.contains("album", case=False) == True]
dfTracks = dfSpotify[dfSpotify['Text'].str.contains("track", case=False) == True]
dfArtists = dfSpotify[dfSpotify['Text'].str.contains("artist", case=False) == True]
dfPlaylists = dfSpotify[dfSpotify['Text'].str.contains("playlist", case=False) == True]

keep_col = ['Text']

dfSpotify = dfSpotify[keep_col]
dfTracks = dfTracks[keep_col]
dfAlbums = dfAlbums[keep_col]
dfArtists = dfArtists[keep_col]
dfPlaylists = dfPlaylists[keep_col]

dfSpotify.to_csv('spotify.txt', index=False)
dfTracks.to_csv('tracks.txt', index=False)
dfAlbums.to_csv('albums.txt', index=False)
dfArtists.to_csv('artists.txt', index=False)
dfPlaylists.to_csv('playlists.txt', index=False)

# Put list into array format
with open('tracks.txt', 'r') as f:
    mySongs = [line.strip() for line in f]
mySongs.pop(0)

# Put the links of the songs into track format
tracks1 = []
tracks2 = []
index = 0
for i in mySongs:
    string = mySongs[index]
    index += 1
    a = string.split("/")
    myStr = a[4]
    ids = myStr.split("?")
    trackId = ids[0]
    correctFormat = "spotify:track:"+ trackId
    if (len(tracks1) < 100):
        tracks1.append(correctFormat)
    else:
        tracks2.append(correctFormat)

#sample_tracks = ['spotify:track:0E9ZjEAyAwOXZ7wJC0PD33', 'spotify:track:1Bqxj0aH5KewYHKUg1IdrF']
spotifyObject.user_playlist_replace_tracks(username, playlist_id, tracks1)
spotifyObject.user_playlist_add_tracks(username, playlist_id, tracks2)
