import graphclass
import matplotlib.pyplot as plt


if __name__ == '__main__':
    graph = graphclass._Song_Graph()
    for attribute in {'danceability', 'energy', 'instrumentalness', 'loudness', 'speechiness', 'tempo', 'valence'}:
        graph.read_csv_data("cleaned_spotify_songs.csv")
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
        plt.savefig(f'average_{attribute}.png')
        plt.show()
