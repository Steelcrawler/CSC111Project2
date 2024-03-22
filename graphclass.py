"""CSC111 Exercise 3: Graphs and Recommender Systems (Part 1)

Module Description
==================
This module contains the _Vertex and Graph classes from lecture, along with some additional
methods that you'll implement in this exercise.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""
from __future__ import annotations
from typing import Any, Optional


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
        self.neighbours = {}h

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

class _Song_Graph(Graph):
    ''' A graph of attribute ranges, with neighbors of the attribute ranges being the songs

    Representation Invariants:
        - all(isinstance(self._vertices[item], _Attribute_Vertex) for item in self._vertices)
    '''
    _vertices: dict[(str, str), _Vertex]

    def __init__(self) -> None:
        super().__init__()
        for i in range(0, 10):
            interval = str(round(i*0.1, 2)) + '-' + str(round((i+1)*0.1, 2))
            self._vertices[('valence', interval)] = _Attribute_Vertex('valence', interval)
        for i in range(0, 10):
            interval = str(round(i*0.1, 2)) + '-' + str(round((i+1)*0.1, 2))
            self._vertices[('energy', interval)] = _Attribute_Vertex('energy', interval)
        for i in range(0, 10):
            interval = str(round(i*0.1, 2)) + '-' + str(round((i+1)*0.1, 2))
            self._vertices[('danceability', interval)] = _Attribute_Vertex('danceability', interval)
        for i in range(0, 10):
            interval = str(round(i*0.1, 2)) + '-' + str(round((i+1)*0.1, 2))
            self._vertices[('loudness', interval)] = _Attribute_Vertex('loudness', interval)
        for i in range(0, 10):
            interval = str(round(i*0.1, 2)) + '-' + str(round((i+1)*0.1, 2))
            self._vertices[('instrumentalness', interval)] = _Attribute_Vertex('instrumentalness', interval)
        for i in range(0, 10):
            interval = str(round(i*0.1, 2)) + '-' + str(round((i+1)*0.1, 2))
            self._vertices[('tempo', interval)] = _Attribute_Vertex('tempo', interval)
        for i in range(0, 10):
            interval = str(round(i*0.1, 2)) + '-' + str(round((i+1)*0.1, 2))
            self._vertices[('speechiness', interval)] = _Attribute_Vertex('speechiness', interval)

def create_Attribute_Vertices(num_splits: int, attribute: str) -> lst[_Attribute_Vertex]:
    ''' Create a list of attribute vertices for a given attribute
    '''
    vertices = []
    for i in range(0, num_splits):
        interval = str(round(i*1/num_splits, 2)) + '-' + str(round((i+1)*1/num_splits, 2))
        vertices.append(_Attribute_Vertex(attribute, interval))
    return vertices



class _Song_Vertex(_Vertex):
    ''' A song vertex in a graph
    '''
    song_name: str
    artist: str
    song_id: str

    def __init__(self, song_name: str, artist: str, song_id: str, neighbours: set[_Vertex]) -> None:
        super().__init__(neighbours)
        self.song_name = song_name
        self.artist = artist
        self.song_id = song_id


class _Attribute_Vertex(_Vertex):
    ''' An attribute vertex in a graph
    '''
    attribute: str
    interval: str

    def __init__(self, attribute: str, interval: str, neighbours: set[_Vertex]) -> None:
        super().__init__(neighbours)
        self.attribute = attribute
        self.interval = interval
