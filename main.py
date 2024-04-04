"""CSC111 Project 2

Error Explanations:
[Line 34] Forbidden top-level code found on line 39
Reasoning: Need this line of code to create the flask app

[Line 35] Forbidden top-level code found on line 40
Reasoning: Need this global variable to store the recommended songs throughout the different app routes

[Line 34] Global variables must be constants or type aliases in CSC108/CSC148: a global variable 'app' is assigned to
on line 11
Reasoning: Need this line of code to create the flask app

[Line 35/105/123] Global variables must be constants or type aliases in CSC108/CSC148: the keyword 'global' is used
Reasoning: Need this global variable to store the recommended songs throughout the different app routes

[Line 34] Constant name "app" should be in UPPER_CASE_WITH_UNDERSCORES format. Constants should be all-uppercase words
with each word separated by an underscore. A single leading underscore can be used to denote a private constant.
Reasoning: flask app documentation uses app in lower case

[Line 35] Every global variable can be referenced from the module level, so using the 'global' keyword at the module
level has no effect.
Reasoning: Need to initialize global variable before use in the module level

"""
import doctest
from typing import Any
import python_ta
from flask import Flask, Response, redirect, render_template, request
import graphclass
import popularity_3d_graph
from spotify_playlist_generator import create_playlist_with_username

app = Flask(__name__)
global RECOMMENDED_SONGS_GLOBAL
DROPDOWN_OPTIONS = {
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
    global DROPDOWN_OPTIONS

    return render_template('index2.html', dropdown_options=DROPDOWN_OPTIONS)


def dictionary_obtainer() -> dict[Any, str]:
    """ Obtain the selected options from dropdowns.
    """
    selected_options = []
    dict_of_return = {}
    for i in range(1, 8):
        dropdown_value = request.form.get(
            f'dropdown_{i}')  # Iterate over dropdown identifiers (as they are named dropdown_1 to dropdown_7)
        if dropdown_value:  # Check if a dropdown value was selected
            selected_options.append(
                dropdown_value)  # Store the selected option in the dictionary with its dropdown identifier as the key
        dict_of_return[f'dropdown_{i}'] = dropdown_value

    def get_new(dictionary: dict[str, dict], dict_of_return_var: dict[str, str]) -> dict[Any, int]:
        """ Helper function to obtain the dictionary.
        """
        new_dict = {}
        for val in dict_of_return_var:  # Iterate over each variable in the provided dictionary from the user input.
            row = dictionary[val]  # Get the smaller dictionary corresponding to the current variable
            lst = [i + 1 for i in range(len(row['options'])) if
                   row['options'][i] == dict_of_return_var[val]]
            if lst:  # if list an option is found
                new_dict[row['label']] = int(
                    lst[0])  # Store the label of the variable and its corresponding index in the new dictionary.
        return new_dict

    # Call the helper function to obtain the processed dictionary
    dict2 = get_new(DROPDOWN_OPTIONS, dict_of_return)
    obtained_dict = {}
    for var in dict2:
        obtained_dict[var] = graphclass.get_range_str_from_index(dict2[var], graphclass.get_attribute_range(var),
                                                                 graphclass.get_num_splits(var))

    return obtained_dict  # Returns a dictionary where keys are variable labels and values are processed range strings


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
    my_graph = graphclass.SongGraph()  # Create an instance of the SongGraph class
    my_graph.read_csv_data('cleaned_spotify_songs.csv')
    result_dictionary = dictionary_obtainer()
    # Obtain a dictionary of variables mapped to the ranges for recommending songs
    recommended_songs = my_graph.reccomend_songs(**result_dictionary)
    # Get recommended songs from the SongGraph instance based on the obtained dictionary
    global RECOMMENDED_SONGS_GLOBAL
    if len(recommended_songs) > 100:
        RECOMMENDED_SONGS_GLOBAL = recommended_songs[:100]

    if len(recommended_songs) > 20:
        recommended_songs = recommended_songs[:20] + ['and more!']
        recommended_songs = ', '.join(recommended_songs)

    return render_template('result.html', recommended_songs=recommended_songs)
    # Return a rendered template 'result.html' with the recommended songs


@app.route('/create_playlist', methods=['POST'])
def create_playlist() -> Response:
    """ Create a Spotify Playlist.
    """
    # Retrieve the Spotify username URL and recommended songs from the form
    spotify_username = request.form.get('spotify_username')
    spotify_username = spotify_username.split('/')[-1]
    global RECOMMENDED_SONGS_GLOBAL
    create_playlist_with_username(RECOMMENDED_SONGS_GLOBAL, spotify_username)

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
    doctest.testmod()
    python_ta.check_all(config={
        'extra-imports': ['os', 'flask', 'graphclass', 'popularity_3d_graph', 'adi_spotify_playlist_gen',
                          'spotify_playlist_generator'],
        'allowed-io': ['create_playlist'],
        'max-line-length': 120
    })
