import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set up of the Spotify API credentials
client_id = '59908f48513949c2a60ab7320c8b1bc5'
client_secret = 'd2009d6c693848b5a5519f8af0e89738'
redirect_uri = 'http://localhost:8080'  # You can set this to your desired redirect URI

# Create a SpotifyOAuth object
sp_oauth = SpotifyOAuth(client_id = client_id, client_secret = client_secret, redirect_uri = redirect_uri, scope = 'playlist-modify-private')

# Get the authorization URL
auth_url = sp_oauth.get_authorize_url()

# Ask the Spotify user to authorize the app and get the authorization code
print("Please go to this URL and authorize access: {}".format(auth_url))
auth_code = input("Enter the authorization code: ")

# Get the access token
token_info = sp_oauth.get_access_token(auth_code)
access_token = token_info['access_token']

# Create a Spotify object
sp = spotipy.Spotify(auth = access_token)

# Create a new playlist
playlist_name = "Your Playlist Name"
playlist_description = "Your Playlist Description"
user_id = sp.current_user()['id']
playlist = sp.user_playlist_create(user_id, playlist_name, public = False, description = playlist_description)

# Print the created playlist details
print("Playlist '{}' created successfully.".format(playlist_name))
print("Playlist ID:", playlist['id'])
