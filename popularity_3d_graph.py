"""CSC111 Project 2

Error Explanations:
[Line 23/25] Since _vertices starts with an underscore, it is considered private and so should not be accessed outside
the class in which it is defined.
Reasoning: Need access to the vertices of the graph to get the songs associated with those values

[Line 14] Imports from package plotly are not grouped
Reasoning: Imports use different names for different modules
"""
import doctest
import plotly.graph_objects as go
import python_ta
import plotly.offline as pyo
import graphclass


def calculate_popularity_attribute(attribute: str, graph: graphclass.SongGraph) -> dict:
    """ Calculate the popularity for a specific attribute.
    """
    range_to_popularity = {}  # similar to popularitygraphgenerator.py, maos attribute range to average popularity

    for vertex in graph._vertices:
        if vertex[0] == attribute:  # checks if that is the attribute we are looking for
            neighbors = graph._vertices[vertex].neighbours
            if len(neighbors) == 0:  # sets value to 0 in case there are no songs in that range
                range_to_popularity[vertex[1]] = 0
            else:
                total_popularity = sum([int(neighbor.track_popularity) for neighbor in neighbors])
                average_popularity = total_popularity / len(neighbors)
                range_to_popularity[vertex[1]] = average_popularity

    percentile_to_popularity = {}  # turns the attribute range mapping into a percentile mapping for normalization
    for key in range_to_popularity:
        percentile = graphclass.reverse_value_range(key, graphclass.get_attribute_range(attribute), 10)
        percentile_to_popularity[percentile] = range_to_popularity[key]
    return percentile_to_popularity  # dictionary with percentile mapping to average popularity


def get_data_for_graph() -> dict:
    """ Retrieve a song data from a CSV file and organize it for the visualization.
    """
    graph = graphclass.SongGraph(stats=True)
    graph.read_csv_data("cleaned_spotify_songs.csv")
    attribute_to_dict = {}  # uses calculate_populatiy_attribute on every attribute
    for attribute in {'danceability', 'energy', 'instrumentalness', 'loudness', 'speechiness', 'tempo', 'valence'}:
        popularity = calculate_popularity_attribute(attribute, graph)
        attribute_to_dict[attribute] = popularity
    return attribute_to_dict


def generate_heatmap() -> None:
    """ Generate a Heatmap visualization.
    """
    attribute_to_dict = get_data_for_graph()  # gets all the data from the graph
    x_values = []
    y_values = []
    z_values = []

    for attribute, value_dict in attribute_to_dict.items():
        for key, value in value_dict.items():
            x_values.append(attribute)  # the x-axis is the attributes
            y_values.append(key)  # the y-axis is the percentiles
            z_values.append(0 if value is None else value)  # the heat values is the popularity

    fig = go.Figure(data=go.Heatmap(  # generating a heatmap using the values
        x=x_values,
        y=y_values,
        z=z_values,
        colorscale='Jet',
        colorbar={"title": 'Popularity'},
    ))

    # Add labels to the axes
    fig.update_layout(
        title='Heatmap of Attributes',
        xaxis_title='Attributes',
        yaxis_title='Percentiles (measured in 10% increments)',
        autosize=False,
        width=500,
        height=500,
        margin={"l": 65, "r": 50, "b": 65, "t": 90}
    )

    # Show the figure
    fig.show()
    # pio.write_image(fig, 'heatmap.png') # save the image to the directory


def generate_3d_graph() -> None:
    """ Generate a 3D visualization of the data. This will only show the 3D visualization when run, but does
    not genreate a div element.
    """
    attribute_to_dict = get_data_for_graph()  # gets all the data from the graph
    x_values = []
    y_values = []
    z_values = []

    for attribute, value_dict in attribute_to_dict.items():
        for key, value in value_dict.items():
            x_values.append(attribute)  # the x-axis is the attributes
            y_values.append(key)  # the y-axis is the percentiles
            z_values.append(0 if value is None else value)  # the z-axis is the popularity

    # Create the 3D scatter plot
    fig = go.Figure(data=go.Scatter3d(
        x=x_values,
        y=y_values,
        z=z_values,
        mode='markers',
        marker={"size": 3, "color": z_values, "colorscale": 'Viridis', "opacity": 0.8},
    ))

    # Add labels to the axes
    fig.update_layout(
        title='3D Scatter Plot of Attributes',
        scene={"xaxis_title": 'Attributes', "yaxis_title": 'Percentile (in 10% increments)',
               "zaxis_title": 'Popularity'},
        autosize=False,
        width=500,
        height=500,
        margin={"l": 65, "r": 50, "b": 65, "t": 90}
    )
    fig.update_yaxes(categoryorder='category ascending')

    # Show the figure
    fig.show()


def generate_div_graph() -> str:
    """ Generate a Plotly Div string for embedding the visualization. The code is the same as generate_3d_graph(),
    but it generates a div html element to be added into the website
    """
    attribute_to_dict = get_data_for_graph()
    x_values = []
    y_values = []
    z_values = []

    for attribute, value_dict in attribute_to_dict.items():
        for key, value in value_dict.items():
            x_values.append(attribute)
            y_values.append(key)
            z_values.append(0 if value is None else value)

    # Create the 3D scatter plot
    fig = go.Figure(data=go.Scatter3d(
        x=x_values,
        y=y_values,
        z=z_values,
        mode='markers',
        marker={"size": 3, "color": z_values, "colorscale": 'Viridis', "opacity": 0.8}
    ))

    # Add labels to the axes
    fig.update_layout(
        title='3D Plot of Attributes, their Percentile, and Popularity',
        scene={"xaxis_title": 'Attributes', "yaxis_title": 'Percentile (in 10% increments)',
               "zaxis_title": 'Popularity'},
        autosize=False,
        width=500,
        height=500,
        margin={"l": 65, "r": 50, "b": 65, "t": 90}
    )
    fig.update_yaxes(categoryorder='category ascending')
    div = pyo.plot(fig, output_type='div')  # saves the graph as a div element
    return div


if __name__ == '__main__':
    doctest.testmod()
    python_ta.check_all(config={
        'extra-imports': ['plotly.graph_objects', 'graphclass', 'math', 'plotly.io', 'plotly.offline'],
        'allowed-io': ['add_song', 'reccomend_songs', 'read_csv_data'],
        'max-line-length': 120
    })
