"""CSC111 Project 2"""
import doctest
import python_ta
import spotipy
from spotipy import util


def create_playlist(songs: list) -> None:
    """ Create a playlist for a given user and add songs to it on Spotify.

    Preconditions:
        - songs != []
        - all(len(song) > 0 for song in songs)
    """
    client_id = 'abacd94498c945af91633a3e85ed1fa1'
    client_secret = '8f38ae574af4484c91c0e95f412c4ffe'
    # redirect_uri = 'http://localhost:8888/callback'

    username = input('Enter the link to your Spotify profile (Click on your icon on the top right, '
                     'click profile, and copy paste the link here):')
    username = username.split('/')[-1]
    token = util.prompt_for_user_token(
        username=username,
        scope='playlist-modify-private playlist-modify-public',
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://localhost:8888/callback"
    )
    spotify = spotipy.Spotify(auth=token)
    playlist_name = 'Reccomended Playlist For You!'
    playlist = spotify.user_playlist_create(user=username, name=playlist_name, public=False,
                                            description='Playlist generated using CSC111 project 2!')
    for song in songs:
        results = spotify.search(q='track:' + song, type='track', limit=1)
        items = results['tracks']['items']
        if len(items) > 0:
            track = items[0]
            track_id = track['id']
            spotify.playlist_add_items(playlist['id'], [track_id])


def create_playlist_with_username(songs: list, username: str) -> None:
    """ Create a playlist for a given user and add songs to it on Spotify.

    Preconditions:
        - songs != []
        - username != ''
        - all(len(song) > 0 for song in songs)
    """
    client_id = 'abacd94498c945af91633a3e85ed1fa1'
    client_secret = '8f38ae574af4484c91c0e95f412c4ffe'

    token = util.prompt_for_user_token(
        username=username,
        scope='playlist-modify-private playlist-modify-public',
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://localhost:8888/callback"
    )
    spotify = spotipy.Spotify(auth=token)

    playlist_name = 'Reccomended Playlist For You!'
    playlist = spotify.user_playlist_create(user=username, name=playlist_name, public=False, description='test playlist'
                                            )
    for song in songs:
        results = spotify.search(q='track:' + song, type='track', limit=1)
        items = results['tracks']['items']
        if len(items) > 0:
            track = items[0]
            track_id = track['id']
            spotify.playlist_add_items(playlist['id'], [track_id])


if __name__ == '__main__':
    doctest.testmod()
    python_ta.check_all(config={
        'extra-imports': ['spotipy', 'spotipy.util', 'spotipy.oauth2'],
        'allowed-io': ['create_playlist'],
        'max-line-length': 120
    })
