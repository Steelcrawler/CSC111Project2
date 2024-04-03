"""CSC111 Project 2"""
# import os
from typing import Any

import python_ta
from flask import Flask, Response, redirect, render_template, render_template_string, request
# from flask import session
import graphclass
import popularity_3d_graph
from spotify_playlist_generator import create_playlist_with_username

app = Flask(__name__)
global reccomended_songs_global
# app.secret_key = 'bruhmoment'
dropdown_options = {
    'dropdown_1': {'label': 'loudness', 'options': ['Whisper', 'Quiet', 'Medium', 'Loud', 'No Eardrums']},
    'dropdown_2': {'label': 'tempo', 'options': ['Snail', 'Slow', 'Medium', 'Fast', 'Cheetah']},
    'dropdown_3': {'label': 'speechiness', 'options': ['No Words', 'Some', 'Lotta Words']},
    'dropdown_4': {'label': 'valence',
                   'options': ['Depression', 'In my room blues', 'Sorta Happy', 'Dancing on the street', 'On Drugs']},
    'dropdown_5': {'label': 'energy', 'options': ['Low', 'Medium', 'High', 'Hyperactive']},
    'dropdown_6': {'label': 'danceability',
                   'options': ['No dancing', 'Get a little jiggy', 'Club vibes', 'U wanna be Beyonce']},
    'dropdown_7': {'label': 'instrumentalness', 'options': ['None', 'Some', 'Only instruments']}
}


@app.route('/')
def index() -> str:
    """ Render the index page with dropdown options.
    """
    global dropdown_options

    return render_template('index2.html', dropdown_options=dropdown_options)


def dictionary_obtainer() -> dict[Any, str]:
    """ Obtain the selected options from dropdowns.
    """
    selected_options = []
    dict_of_return = {}
    for i in range(1, 8):
        dropdown_value = request.form.get(f'dropdown_{i}')
        if dropdown_value:
            selected_options.append(dropdown_value)
        dict_of_return[f'dropdown_{i}'] = dropdown_value

    def get_new(dictionary: dict[str, dict], dict_of_return_var: dict[str, str]) -> dict[Any, int]:
        """ Helper function to obtain the dictionary.
        """
        new_dict = {}
        for val in dict_of_return_var:
            row = dictionary[val]
            lst = [i + 1 for i in range(len(row['options'])) if
                   row['options'][i] == dict_of_return_var[val]]
            if lst:
                new_dict[row['label']] = int(lst[0])
        return new_dict

    dict2 = get_new(dropdown_options, dict_of_return)
    obtained_dict = {}
    for var in dict2:
        obtained_dict[var] = graphclass.get_range_str_from_index(dict2[var], graphclass.get_attribute_range(var),
                                                                 graphclass.get_num_splits(var))

    return obtained_dict


# @app.route('/result', methods=['POST'])
# def result():
#     my_graph=graphclass._Song_Graph()
#     my_graph.read_csv_data('cleaned_spotify_songs.csv')
#     result_dictionary = dictionary_obtainer()
#     return my_graph.reccomend_songs(**result_dictionary)

@app.route('/result', methods=['POST'])
def result() -> str:
    """ Render the result with recommended songs.
    """
    my_graph = graphclass.SongGraph()
    my_graph.read_csv_data('cleaned_spotify_songs.csv')
    result_dictionary = dictionary_obtainer()
    recommended_songs = my_graph.reccomend_songs(**result_dictionary)
    global reccomended_songs_global
    if len(recommended_songs) > 100:
        reccomended_songs_global = recommended_songs[:100]

    if len(recommended_songs) > 20:
        recommended_songs = recommended_songs[:20] + ['and more!']
        recommended_songs = ', '.join(recommended_songs)
    
    return render_template('result.html', recommended_songs=recommended_songs)


@app.route('/create_playlist', methods=['POST'])
def create_playlist() -> Response:
    """ Create a Spotify Playlist.
    """
    # Retrieve the Spotify username URL and recommended songs from the form
    spotify_username = request.form.get('spotify_username')
    spotify_username = spotify_username.split('/')[-1]
    global reccomended_songs_global
    # Perform actions to create the playlist in Spotify using the username and recommended songs
    print(reccomended_songs_global[0])
    # print(reccomended_songs_global[0], type(reccomended_songs_global[0]))
    create_playlist_with_username(reccomended_songs_global, spotify_username)

    # Redirect the user to their Spotify profile where they can view the created playlist
    spotify_profile_url = f"https://open.spotify.com/user/{spotify_username}"
    return redirect(spotify_profile_url)


@app.route('/danceabilitygraph')
def danceabilitygraph() -> str:
    """ Render the danceability graph.
    """
    return render_template('danceabilityimage.html')


@app.route('/energygraph')
def energygraph() -> str:
    """ Render the energy graph.
    """
    return render_template('energyimage.html')


@app.route('/instrumentalnessgraph')
def instrumentalnessgraph() -> str:
    """ Render the instrumentalness graph.
    """
    return render_template('instrumentalnessimage.html')


@app.route('/loudnessgraph')
def loudnessgraph() -> str:
    """ Render the loudness graph.
    """
    return render_template('loudnessimage.html')


@app.route('/speechinessgraph')
def speechinessgraph() -> str:
    """ Render the speechiness graph.
    """
    return render_template('speechinessimage.html')


@app.route('/tempograph')
def tempograph() -> str:
    """ Render the tempo graph.
    """
    return render_template('tempoimage.html')


@app.route('/valencegraph')
def valencegraph() -> str:
    """ Render the valence graph.
    """
    return render_template('valenceimage.html')


@app.route('/heatmap')
def heatmap() -> str:
    """ Render the heatmap graph.
    """
    return render_template('heatmap.html')


@app.route('/3Dgraph')
def draw3dgraph() -> str:
    """ Render the 3D graph.
    """
    div = popularity_3d_graph.generate_div_graph()
    return render_template('3Dgraph.html', div=div)


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 7899)))
    python_ta.check_all(config={
        'extra-imports': ['os', 'flask', 'graphclass', 'popularity_3d_graph', 'adi_spotify_playlist_gen'],
        'allowed-io': ['create_playlist'],
        'max-line-length': 120
    })
