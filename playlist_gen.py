# splits, creates, & populates playlist for data collection
# 1-23-21

# == imports == #
import os
import spotipy 
import pandas as pd

# == main == #
# env variables
CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
USERNAME = os.environ.get('SPOTIFY_USERNAME')

# spotify auth 
token = spotipy.util.prompt_for_user_token(
    username=USERNAME,
    scope='playlist-modify-private', 
    client_id=CLIENT_ID, 
    client_secret=CLIENT_SECRET, 
    redirect_uri='http://localhost:8888/callback' # registered with spotify
)

sp = spotipy.Spotify(auth=token)
user = sp.current_user()

# create & populate playlists 
playlist_count = 5
playlists = np.array_split(ce_df,playlist_count)

for i in range(playlist_count):
    playlist = sp.user_playlist_create(
        user = user['id'],
        name = f'ce_{i+1}',
        public = False,
        collaborative=False,
        description=''
    )
    sp.user_playlist_add_tracks(
        user = user['id'],
        playlist_id = playlist['id'],
        tracks = playlists[i]['id'] # track ids
    )

    playlists[i].name = playlists[i].name.apply(lambda x: x[:30]) # shorten names
    playlists[i][['name']].to_excel(f'forms/ce_{i+1}.xlsx', index=False)
