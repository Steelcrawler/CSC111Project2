import python_ta
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util

client_id = 'abacd94498c945af91633a3e85ed1fa1'
client_secret = '8f38ae574af4484c91c0e95f412c4ffe'
redirect_uri = 'http://localhost:8888/callback'

# Authenticate the user and get an access token
username = input('What\'s your spotify username?')
token = util.prompt_for_user_token(
    username=username,
    scope='playlist-modify-private playlist-modify-public',
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri="http://localhost:8888/callback"
)
spotify = spotipy.Spotify(auth=token)
song_name = 'Bandit'  # replace with your song name

# # Create the playlist
playlist_name = 'test_playlist'
playlist = spotify.user_playlist_create(user=username, name=playlist_name, public=False, description='test playlist')

# Search for the song
results = spotify.search(q='track:' + song_name, type='track', limit=1)
items = results['tracks']['items']
if len(items) > 0:
    track = items[0]
    track_id = track['id']
    spotify.playlist_add_items(playlist['id'], [track_id])
