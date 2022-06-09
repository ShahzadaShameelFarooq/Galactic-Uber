"""Assignment 2 - Distance map [Task 1]

CSC148, Summer 2021

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

This module is replicated with permission from the Winter 2021 A1,
created by Diane Horton, Ian Berlott-Attwell, Jonathan Calver,
Sophia Huynh, Maryam Majedi, and Jaisie Sin.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 the Department of Computer Science,
University of Toronto

===== Module Description =====

This module contains the class DistanceMap, which is used to store
and look up distances between intergalactic bodies. This class does not
read distances from the map file. (All reading from files is done in module
a2_command_central.)

Instead, it provides public methods that can be called to store and look up
distances.

"""

from typing import Dict


class DistanceMap:
    _distances: Dict[str, float]

    def __init__(self):
        self._distances = {}

    def distance(self, p: str, q: str) -> float:
        """

        """
        if p + q in self._distances:
            return self._distances[p + q]
        elif q + p in self._distances:
            return self._distances[q + p]
        else:
            return -1

    def add_distance(self, p: str, q: str, n: float) -> None:
        """

        """
        if p + q not in self._distances:
            self._distances[p + q] = n


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing'],
        'disable': ['E1136'],
        'max-attributes': 15
    })
    import doctest

    doctest.testmod()
