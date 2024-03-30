import plotly.graph_objects as go
import graphclass
import math
import plotly.io as pio


if __name__ == '__main__':
    graph = graphclass._Song_Graph(stats=True)
    graph.read_csv_data("cleaned_spotify_songs.csv")
    attribute_to_dict = {}
    for attribute in {'danceability', 'energy', 'instrumentalness', 'loudness', 'speechiness', 'tempo', 'valence'}:
        range_to_popularity = {}
        range_to_count = {}
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
        attribute_to_dict[attribute] = percentile_to_popularity

    # dict_test = attribute_to_dict['danceability']
    # for key in dict_test:
    #     print(f'{key}: {dict_test[key]}')

    x_values = []
    y_values = []
    z_values = []

    for attribute, value_dict in attribute_to_dict.items():
        for key, value in value_dict.items():
            x_values.append(attribute)
            y_values.append(key)
            z_values.append(0 if value is None or math.isnan(value) else value)
    
    # fig = go.Figure(data=go.Heatmap(
    #     x=x_values,
    #     y=y_values,
    #     z=z_values,
    #     colorscale='Jet',
    #     colorbar=dict(
    #     title='Popularity',
    # ),
    # ))

    # # Add labels to the axes
    # fig.update_layout(
    #     title='Heatmap of Attributes',
    #     xaxis_title='Attributes',
    #     yaxis_title='Percentiles (measured in 10% increments)',
    #     autosize=False,
    #     width=500,
    #     height=500,
    #     margin=dict(l=65, r=50, b=65, t=90)
    # )

    # # Show the figure
    # fig.show()
    # pio.write_image(fig, 'heatmap.png')
    

    # Create the 3D scatter plot
    fig = go.Figure(data=go.Scatter3d(
        x=x_values,
        y=y_values,
        z=z_values,
        mode='markers',
        marker=dict(
            size=3,
            color=z_values,  # set color to an array/list of desired values
            colorscale='Viridis',  # choose a colorscale
            opacity=0.8
        )
    ))

    # Add labels to the axes
    fig.update_layout(
        title='3D Scatter Plot of Attributes',
        scene=dict(
            xaxis_title='Attributes',
            yaxis_title='Percentile (in 10% increments)',
            zaxis_title='Popularity',
        ),
        autosize=False,
        width=500,
        height=500,
        margin=dict(l=65, r=50, b=65, t=90)
    )
    fig.update_yaxes(categoryorder='category ascending')
    # Show the figure
    fig.show()