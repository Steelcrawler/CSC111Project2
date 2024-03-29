import plotly.graph_objs as go
from graphclass import _Song_Graph, _Song_Vertex


def convert_range_string_to_tuple(range_string):
    range_split = range_string.split('-')
    if len(range_split) == 2:  # Check if there are two parts in the split
        return (float(range_split[0]), float(range_split[1]))
    else:
        return None


my_graph = _Song_Graph()
my_graph.read_csv_data('cleaned_spotify_songs.csv')
valence = my_graph._vertices[('valence', '0.25-0.5')].neighbours
dancability = my_graph._vertices[('danceability', '0.25-0.5')].neighbours
union_set = valence.union(dancability)
list1 = list(union_set)[:10]
song_attributes = {}
for item in list1:
    song_attributes[item.song_name] = {i.attribute: convert_range_string_to_tuple(i.interval) for i in item.neighbours}

# Sample attribute ranges for each song (replace these with your actual attribute ranges)
sample_song_attributes = {
    'Song1': {'valence': (0.5, 0.7), 'energy': (0.6, 0.8), 'danceability': (0.4, 0.6), 'loudness': (-8, -6), 'instrumentalness': (0.1, 0.3), 'tempo': (100, 120), 'speechiness': (0.1, 0.3), 'artist': 'Artist1'},
    'Song2': {'valence': (0.7, 0.9), 'energy': (0.5, 0.7), 'danceability': (0.6, 0.8), 'loudness': (-10, -8), 'instrumentalness': (0.0, 0.2), 'tempo': (120, 140), 'speechiness': (0.3, 0.5), 'artist': 'Artist2'},
    'Song3': {'valence': (0.6, 0.8), 'energy': (0.7, 0.9), 'danceability': (0.5, 0.7), 'loudness': (-6, -4), 'instrumentalness': (0.1, 0.3), 'tempo': (140, 160), 'speechiness': (0.2, 0.4), 'artist': 'Artist3'},
    'Song4': {'valence': (0.4, 0.6), 'energy': (0.8, 1.0), 'danceability': (0.7, 0.9), 'loudness': (-7, -5), 'instrumentalness': (0.2, 0.4), 'tempo': (110, 130), 'speechiness': (0.2, 0.4), 'artist': 'Artist4'},
    'Song5': {'valence': (0.5, 0.7), 'energy': (0.6, 0.8), 'danceability': (0.5, 0.7), 'loudness': (-8, -6), 'instrumentalness': (0.1, 0.3), 'tempo': (100, 120), 'speechiness': (0.1, 0.3), 'artist': 'Artist5'}
}

# # Extract song names
songs = list(song_attributes.keys())

# Function to create a 3D scatter plot
def create_3d_scatter(x_attribute, y_attribute, z_attribute):
    # Extract attribute ranges for each song and take midpoint
    x_range = [(rng[0] + rng[1]) / 2 for rng in [song_attributes[song][x_attribute] for song in songs]]
    y_range = [(rng[0] + rng[1]) / 2 for rng in [song_attributes[song][y_attribute] for song in songs]]
    z_range = [(rng[0] + rng[1]) / 2 for rng in [song_attributes[song][z_attribute] for song in songs]]

    # Create a 3D scatter plot
    fig = go.Figure(data=[go.Scatter3d(
        x=x_range,
        y=y_range,
        z=z_range,
        mode='markers',
        text=songs,  # Song names as hover text
        hoverinfo='text',
        marker=dict(
            size=10,
            opacity=0.8
        )
    )])

    # Set labels and title
    fig.update_layout(
        scene=dict(
            xaxis_title=x_attribute.capitalize(),
            yaxis_title=y_attribute.capitalize(),
            zaxis_title=z_attribute.capitalize()
        ),
        title=f'{x_attribute.capitalize()}, {y_attribute.capitalize()}, and {z_attribute.capitalize()} Ranges Across Songs',
        hovermode='closest'
    )

    fig.show()

# Ask user to select three attributes
selected_attributes = input("Select three attributes separated by commas from the given options (valence, energy, danceability, loudness, instrumentalness, tempo, speechiness, artist): ").split(',')
create_3d_scatter(*selected_attributes)

# Check if the selected attributes are valid
# if all(attr in song_attributes['Song1'] for attr in selected_attributes) and len(selected_attributes) == 3:
#     create_3d_scatter(*selected_attributes)
# else:
#     print("Invalid attributes. Please select three attributes from the given options.")
