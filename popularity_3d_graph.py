"""CSC111 Project 2"""
# import math
import plotly.graph_objects as go
import python_ta

# import plotly.io as pio
import plotly.offline as pyo
import graphclass


# if __name__ == '__main__':

def get_data_for_graph() -> dict:
    """ Retrieve a song data from a CSV file and organize it for the visualization.
    """
    graph = graphclass.SongGraph(stats=True)
    graph.read_csv_data("cleaned_spotify_songs.csv")
    attribute_to_dict = {}
    for attribute in {'danceability', 'energy', 'instrumentalness', 'loudness', 'speechiness', 'tempo', 'valence'}:
        popularity = calculate_popularity_attribute(attribute, graph)
        attribute_to_dict[attribute] = popularity
    return attribute_to_dict


def calculate_popularity_attribute(attribute: str, graph: graphclass.SongGraph) -> dict:
    """ Calculate the popularity for a specific attribute.
    """
    range_to_popularity = {}

    for vertex in graph._vertices:
        if vertex[0] == attribute:
            neighbors = graph._vertices[vertex].neighbours
            if len(neighbors) == 0:
                range_to_popularity[vertex[1]] = 0
            else:
                total_popularity = sum([int(neighbor.track_popularity) for neighbor in neighbors])
                average_popularity = total_popularity / len(neighbors)
                range_to_popularity[vertex[1]] = average_popularity

    # if attribute == 'danceability':
    #     for key in range_to_popularity:
    #         print(f'{key}: {range_to_popularity[key]}')
    #         print(graphclass.reverse_value_range(key, graphclass.get_attribute_range(attribute), 10))
    percentile_to_popularity = {}
    for key in range_to_popularity:
        percentile = graphclass.reverse_value_range(key, graphclass.get_attribute_range(attribute), 10)
        percentile_to_popularity[percentile] = range_to_popularity[key]
    return percentile_to_popularity


def generate_heatmap() -> None:
    """ Generate a Heatmap visualization.
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

    fig = go.Figure(data=go.Heatmap(
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
    # pio.write_image(fig, 'heatmap.png')


def generate_3d_graph() -> None:
    """ Generate a 3D visualization.
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
    """ Generate a Plotly Div string for embedding the visualization.
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
    div = pyo.plot(fig, output_type='div')
    return div


if __name__ == '__main__':
    python_ta.check_all(config={
        'extra-imports': ['plotly.graph_objects', 'graphclass', 'math', 'plotly.io', 'plotly.offline'],
        'allowed-io': ['add_song', 'reccomend_songs', 'read_csv_data'],
        'max-line-length': 120
    })
