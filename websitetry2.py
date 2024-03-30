import os

from flask import Flask, jsonify, render_template, request
from graphclass import get_range_str_from_index, get_num_splits, get_attribute_range

app = Flask(__name__)

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
def index():
    global dropdown_options
    # Define the dropdown options dynamically

    return render_template('index2.html', dropdown_options=dropdown_options)


@app.route('/result', methods=['POST'])
def result():
    selected_options = []
    dict_of_return = {}
    for i in range(1, 8):
        dropdown_value = request.form.get(f'dropdown_{i}')
        if dropdown_value:
            selected_options.append(dropdown_value)
        dict_of_return[f'dropdown_{i}'] = dropdown_value

    def get_new(dictionary, dict_of_return_var):
        newdict = {}
        for val in dict_of_return_var:
            row = dictionary[val]
            lst= [i+1 for i in range(len(row['options'])) if
                                     row['options'][i] == dict_of_return_var[val]]
            if lst:
                newdict[row['label']]=int(lst[0])
        return newdict

    dict2=get_new(dropdown_options,dict_of_return)
    final_effing_thing={}
    for var in dict2:
        final_effing_thing[var]=get_range_str_from_index(dict2[var], get_attribute_range(var), get_num_splits(var))
        print(final_effing_thing)

    return final_effing_thing






if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8876)))
