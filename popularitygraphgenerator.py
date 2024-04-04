"""CSC111 Project 2

Error Explanations:
[Line 33] Disallowed name "bar". You should give your variables meaningful rather than generic names.
Reasoning: This is literally the name for each bar in the bar graph

[Line 35] Since _vertices starts with an underscore, it is considered private and so should not be accessed outside
the class in which it is defined.
Reasoning: Access to vertices of the graph object to generate a visual graph

[Line 46] Since _vertices starts with an underscore, it is considered private and so should not be accessed outside
the class in which it is defined.
Reasoning: Access to vertices of the graph object to generate a visual graph
"""
import doctest
import python_ta
import matplotlib.pyplot as plt
import graphclass


if __name__ == '__main__':
    doctest.testmod()
    python_ta.check_all(config={
        'extra-imports': ['graphclass', 'matplotlib.pyplot'],
        'allowed-io': ['create_playlist'],
        'max-line-length': 120
    })
    graph = graphclass.SongGraph(stats=True)
    graph.read_csv_data("cleaned_spotify_songs.csv")
    for attribute in {'danceability', 'energy', 'instrumentalness', 'loudness', 'speechiness', 'tempo', 'valence'}:
        range_to_popularity = {}
        range_to_count = {}
        for vertex in graph._vertices:
            if vertex[0] == attribute:
                neighbors = graph._vertices[vertex].neighbours
                if len(neighbors) == 0:
                    pass
                else:
                    total_popularity = sum([int(neighbor.track_popularity) for neighbor in neighbors])
                    average_popularity = total_popularity / len(neighbors)
                    range_to_popularity[vertex[1]] = average_popularity
                    range_to_count[vertex[1]] = len(neighbors)

        plt.figure(figsize=(12, 6))
        bars = plt.bar(range_to_popularity.keys(), range_to_popularity.values(), width=0.5)
        for bar, count in zip(bars, range_to_count.values()):
            plt.text(bar.get_x() + (bar.get_width() / 2), bar.get_height(), f'n={count}', ha='center', va='bottom')
        plt.xticks(rotation=90)
        plt.xlabel('Attribute Range')
        plt.ylabel('Average Popularity')
        plt.title(f'Average Popularity by Attribute Range for {attribute.capitalize()}')
        plt.tight_layout()
        # plt.savefig(f'average_{attribute}.png')
        plt.show()
