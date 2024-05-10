"""CSC111 Project 2"""
import doctest
import python_ta
import spotipy
from spotipy import util
from dotenv import load_dotenv
import os

load_dotenv()


def create_playlist(songs: list) -> None:
    """ Create a playlist for a user based on input from the terminal on Spotify.

    Preconditions:
        - songs != []
        - all(len(song) > 0 for song in songs)
    """
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    # To use this yourself, do the following:
    # 1. Create a .env file in the same directory as this file.
    # 2. Add the following lines to the .gitignore file:
    #    ```
    #    client_id = 'your_client_id'
    #    client_secret = 'your_client_secret'
    #    ```
    # 3. Replace 'your_client_id' and 'your_client_secret' with your own client id and secret.
    # redirect_uri = 'http://localhost:8888/callback'

    username = input('Enter the link to your Spotify profile (Click on your icon on the top right, '
                     'click profile, and copy paste the link here):')
    username = username.split('/')[-1]
    token = util.prompt_for_user_token(  # get user's credentials
        username=username,
        scope='playlist-modify-private playlist-modify-public',
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://localhost:8888/callback"
    )
    spotify = spotipy.Spotify(auth=token)  # authenticate with the user's credentials
    playlist_name = 'Reccomended Playlist For You!'
    playlist = spotify.user_playlist_create(user=username, name=playlist_name, public=False,
                                            description='Playlist generated using CSC111 project 2!')
    for song in songs:
        results = spotify.search(q='track:' + song, type='track', limit=1)  # seaches spotify for the song
        items = results['tracks']['items']
        if len(items) > 0:
            track = items[0]
            track_id = track['id']
            spotify.playlist_add_items(playlist['id'], [track_id])  # adds song to playlist if found


def create_playlist_with_username(songs: list, username: str) -> None:
    """ Create a playlist for a given user and add songs to it on Spotify.

    Preconditions:
        - songs != []
        - username != ''
        - all(len(song) > 0 for song in songs)
    """
    client_id = 'abacd94498c945af91633a3e85ed1fa1'
    client_secret = '8f38ae574af4484c91c0e95f412c4ffe'

    token = util.prompt_for_user_token(  # get user credentials
        username=username,
        scope='playlist-modify-private playlist-modify-public',
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://localhost:8888/callback"
    )
    spotify = spotipy.Spotify(auth=token)  # authenticate with the user's credentials

    playlist_name = 'Reccomended Playlist For You!'
    # creates the playlist
    playlist = spotify.user_playlist_create(user=username, name=playlist_name, public=False,
                                            description='Playlist generated using CSC111 project 2!')
    for song in songs:
        results = spotify.search(q='track:' + song, type='track', limit=1)  # seaches for songs
        items = results['tracks']['items']
        if len(items) > 0:
            track = items[0]
            track_id = track['id']
            spotify.playlist_add_items(playlist['id'], [track_id])  # adds it to playlist if found


if __name__ == '__main__':
    doctest.testmod()
    python_ta.check_all(config={
        'extra-imports': ['spotipy', 'spotipy.util', 'spotipy.oauth2'],
        'allowed-io': ['create_playlist'],
        'max-line-length': 120
    })
