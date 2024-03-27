from __future__ import annotations
from typing import Any, Optional
import csv

class _Vertex:
    """A vertex in a graph.

    Instance Attributes:
        - item: The data stored in this vertex.
        - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """
    neighbours: set[_Vertex]

    def __init__(self, neighbours: set[_Vertex]) -> None:
        """Initialize a new vertex with the given item and neighbours."""
        self.neighbours = neighbours


class Graph:
    """A graph.

    Representation Invariants:
        - all(item == self._vertices[item].item for item in self._vertices)
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Any) -> None:
        """Add a vertex with the given item to this graph.

        The new vertex is not adjacent to any other vertices.

        Preconditions:
            - item not in self._vertices
        """
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item, set())

    def add_edge(self, item1: Any, item2: Any) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            # Add the new edge
            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            # We didn't find an existing vertex for both items.
            raise ValueError

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            # We didn't find an existing vertex for both items.
            return False


def get_num_splits(attribute: str) -> int:
    ''' Return the number of splits for a given attribute
    '''
    if attribute == 'loudness':
        return 5 # whisper, quiet, medium, loud, no eardrums
    if attribute == 'tempo':
        return 5 # snail, slow, medium, fast, cheetah
    if attribute == 'speechiness':
        return 3 # no talking, some talking, lots of talking
    if attribute == 'valence':
        return 4 # depression, slightly sad, slightly happy, happy
    if attribute == 'energy':
        return 4 # low energy, medium energy, high energy, hyperactive
    if attribute == 'danceability':
        return 4 # no dancing, some dancing, lots of dancing, hyperactive
    if attribute == 'instrumentalness':
        return 3 # no instruments, some instruments, all instruments


def Create_Attribute_Vertices(vertices: dict, attribute: str, attribute_interval: tuple) -> None:
    ''' Create a list of attribute vertices for a given attribute
    '''
    num_splits = get_num_splits(attribute)
    start = attribute_interval[0]
    end = attribute_interval[1]
    interval_size = (end - start) / num_splits
    for i in range(num_splits):
        interval_start = round(start + i * interval_size, 2)
        interval_end = round(start + (i + 1) * interval_size, 2)
        interval = f"{interval_start}-{interval_end}"
        vertices[(attribute, interval)] = _Attribute_Vertex(attribute, interval, set())

def get_value_range(value: float, total_range: tuple, num_splits: int) -> str:
    ''' Get the range in which a given value fallsm where the first number is inclusive and the second number is exclusive
    >>> get_value_range(0.25, (0.0, 1.0), 4)
    0.25-0.5
    >>> get_value_range(0.0, (0.0, 1.0), 4)
    0.0-0.25
    >>> get_value_range(1.0, (0.0, 1.0), 4)
    0.75-1.0
    '''
    start, end = total_range
    split_size = (end - start) / num_splits
    for i in range(num_splits):
        range_start = round(start + i * split_size, 2)
        range_end = round(start + (i + 1) * split_size, 2)
        if range_start <= value < range_end:
            return f"{range_start}-{range_end}"
    return f"{end}-{end + split_size}"  # for the case when value equals to the end of total range
    

class _Song_Vertex(_Vertex):
    ''' A song vertex in a graph
    '''
    song_name: str
    # artist: str
    song_id: str

    def __init__(self, song_name: str, song_id: str, neighbours: set[_Vertex]) -> None:
        super().__init__(neighbours)
        self.song_name = song_name
        # self.artist = artist
        self.song_id = song_id
    
    def add_neighbor(self, vertex: _Vertex) -> None:
        ''' Add an edge between this song vertex and an attribute vertex
        '''
        self.neighbours.add(vertex)
        vertex.neighbours.add(self)


class _Attribute_Vertex(_Vertex):
    ''' An attribute vertex in a graph
    '''
    attribute: str
    interval: str

    def __init__(self, attribute: str, interval: str, neighbours: set[_Vertex]) -> None:
        super().__init__(neighbours)
        self.attribute = attribute
        self.interval = interval


class _Song_Graph(Graph):
    ''' A graph of attribute ranges, with neighbors of the attribute ranges being the songs

    Representation Invariants:
        - all(isinstance(self._vertices[item], _Attribute_Vertex) for item in self._vertices)
    '''

    _vertices: dict[(str, str), _Vertex] # attribute, range for the vertex, and the vertex object itself
    attributes: dict[str, tuple] # general attribute ranges of any song

    def __init__(self) -> None:
        super().__init__()
        self.attributes = {'valence': (0, 1), 'energy': (0, 1.25), 'danceability': (0, 1), 'loudness': (-60, 10),
                      'instrumentalness': (0, 1), 'tempo': (0, 250), 'speechiness':(0, 1)}
        for attribute in self.attributes:
            Create_Attribute_Vertices(self._vertices, attribute, self.attributes[attribute])
        

    def add_song(self, track_name, track_id, valence, energy, danceability, instrumentalness, tempo, speechiness, loudness):
        ''' Add a song to the graph by creating edges between the song and the attribute vertices
        '''
        song_vertex = _Song_Vertex(track_name, track_id, set())
        song_attributes = {'valence': valence, 'energy': energy, 'danceability': danceability, 
                    'loudness': loudness, 'instrumentalness': instrumentalness, 
                    'tempo': tempo, 'speechiness': speechiness}

        for attribute in self.attributes:
            start, end = self.attributes[attribute]
            num_splits = get_num_splits(attribute)
            range_str = get_value_range(song_attributes[attribute], (start, end), num_splits)
            if (attribute, range_str) not in self._vertices:
                print(f"Attribute vertex {attribute} {range_str} not found")
            else:
                song_vertex.add_neighbor(self._vertices[(attribute, range_str)])
    
    def read_csv_data(self, filename: str) -> None:
        ''' Read a csv file of song data and add the songs to the graph
        '''
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                track_name, track_id, valence, energy, danceability, instrumentalness, tempo, speechiness, loudness = row
                self.add_song(track_name, track_id, float(valence), float(energy), 
                              float(danceability), float(instrumentalness), float(tempo), 
                              float(speechiness), float(loudness))
    


if __name__ == '__main__':
    my_graph = _Song_Graph()
    my_graph.read_csv_data('cleaned_spotify_songs.csv')
    for vertex in my_graph._vertices[('valence', '0.25-0.5')].neighbours:
        print(vertex.song_name)