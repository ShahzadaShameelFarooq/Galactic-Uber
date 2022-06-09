"""Assignment 2 - Scheduling Passengers [Task 4]

CSC148, Summer 2021

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

This module is adapted from the Winter 2021 A1, created by Diane
Horton, Ian Berlott-Attwell, Jonathan Calver, Sophia Huynh, Maryam
Majedi, and Jaisie Sin.

Adapted by: Saima Ali and Marina Tawfik

===== Module Description =====

This module contains the abstract FleetScheduler class, as well as the two
subclasses BogoScheduler and GreedyScheduler, which implement the two
scheduling algorithms described in the handout.
"""

import random
from typing import List, Dict, Callable, Any, Tuple, Optional

from a2_space_bikes import Passenger, SpaceBike
from a2_container import PriorityQueue
from a2_distance_map import DistanceMap


class FleetScheduler:
    """A fleet scheduler that decides which passengers will board which space
    bikes, and what route each space bike will take.

    This is an abstract class.  Only child classes should be instantiated.
    """

    def schedule(
            self, passengers: List[Passenger],
            space_bikes: List[SpaceBike],
            verbosity: int = 0
    ) -> Dict[bool, List[Passenger]]:
        """Schedule a list of passengers, <passengers> to board
        the SpaceBikes in <space_bikes>.

        Mutate the SpaceBike objects in <space_bikes> to reflect
        the passengers that have boarded and to update the route
        they will take.

        Return a mapping of bool to a List of passengers, where
        True maps to boarded passengers and False maps to unboarded
        passengers.

        If <verbosity> is greater than zero, print step-by-step details
        regarding the scheduling algorithm as it runs.  This is *only*
        for debugging purposes for your benefit, so the content and
        format of this information is your choice; we will only test your
        code with <verbosity> set zero.
        """
        raise NotImplementedError


class BogoScheduler(FleetScheduler):
    _dmap: DistanceMap

    def __init__(self, _dmap: DistanceMap):
        FleetScheduler.__init__(self)
        self._dmap = _dmap

    def schedule(
            self, passengers: List[Passenger],
            space_bikes: List[SpaceBike],
            verbosity: int = 0
    ) -> Dict[bool, List[Passenger]]:
        """

        """
        result = {True: [], False: []}
        if verbosity == 0:

            random_passengers = []
            for p in passengers:
                random_passengers.append(p)

            random.shuffle(random_passengers)

            for passenger in random_passengers:
                for bike in space_bikes:
                    if bike.board(passenger, self._dmap):
                        result[True].append(passenger)
                if passenger not in result[True]:
                    result[False].append(passenger)
            return result


def _priority_passenger_distance(a: Any,
                                 b: Any) -> bool:
    """Return True if a is smaller than b. """
    a_dist = a[1].distance(a[0].source, a[0].destination)
    b_dist = b[1].distance(b[0].source, b[0].destination)
    return a_dist < b_dist


def _priority_passenger_bid(a: Any,
                            b: Any) -> bool:
    """Return True if a is bigger than b. """
    a_bid = a[0].bid
    b_bid = b[0].bid
    return a_bid > b_bid


def _priority_division(a: Any,
                       b: Any) -> bool:
    """Return True if a has higher priority than b"""
    a_dist = a[1].distance(a[0].source, a[0].destination)
    b_dist = b[1].distance(b[0].source, b[0].destination)
    a_bid = a[0].bid
    b_bid = b[0].bid
    a_val = a_bid / a_dist
    b_val = b_bid / b_dist
    return a_val > b_val


def _priority_spacebike(a: Tuple[SpaceBike, Passenger, DistanceMap],
                        b: Tuple[SpaceBike, Passenger, DistanceMap]) -> bool:
    """Return True if a has greater priority than b."""
    min_fuel_a = (a[2].distance(a[0].route[-1], a[1].destination) *
                  a[0].fuel_usage_rate)
    min_fuel_b = b[2].distance(b[0].route[-1], b[1].destination) \
                 * b[0].fuel_usage_rate

    if (a[0].max_capacity < b[0].max_capacity
            and (a[1].source in a[0].route and
                 a[1].destination in
                 a[0].route) and (a[0].route.index(a[1].source)
                                  < a[0].route.index(a[1].destination))):
        return True

    elif (a[0].max_capacity > b[0].max_capacity
          and (b[1].source in b[0].route and b[1].destination in b[0].route)
          and (b[0].route.index(b[1].source)
               < a[0].route.index(a[1].destination))):
        return False

    elif min_fuel_a < min_fuel_b:
        return True

    elif min_fuel_a == min_fuel_b:
        if a[0].max_capacity < b[0].max_capacity:
            return True
        elif a[0].max_capacity == b[0].max_capacity:
            if a[0].id_number < b[0].id_number:
                return True
            else:
                return False
        else:
            return False
    else:
        return False


class GreedyScheduler(FleetScheduler):
    """A scheduler using various best options
    to assign the passengers into spacebikes

    === Private Attribute ===
    _mapping: the DistanceMap object that will be used to board the passengers
    _function: priority function being used for boarding the passengers.
    Functions are assigned depending on the self._function

    === Representation Invariants ===
    - _dmap contains all the distance information needed
    - Inputting 'travel dist' as a second parameter will determine
    _function to be _prioritize_close function
    - Inputting 'fare_bid' as a second parameter will determine _function to be
    _prioritize_fare function
    - Inputting 'fare_per_dist' as a second parameter will determine
    _function to be _prioritize_fare_per_distance function
    - _function can only be the mentioned three
    === Sample Usage ===
    >>> dmap = DistanceMap()
    >>> dmap.add_distance("Earth", "Mars", 0.5)
    >>> dmap.add_distance("Mars", "Venus", 1.0)
    >>> greedy = GreedyScheduler(dmap, "fare_bid")
    >>> greedy._dmap == dmap
    True
    >>> p1 = Passenger("Al Roger", 1.0, "Earth", "Mars")
    >>> p2 = Passenger("Sean", 1.5, "Earth", "Mars")
    >>> p3 = Passenger("Jurena", 1.2, "Earth", "Venus")
    >>> b1 = SpaceBike(198161, 'Nova Bike', 2, 8.0, 0.5)
    >>> passengers = [p1, p2, p3]
    >>> bikes = [b1]
    >>> greedy_scheduled = greedy.schedule(passengers, bikes)
    >>> p2.onboard
    True
    >>> p3.onboard
    True
    >>> p1.onboard
    False
    >>> greedy_scheduled[True][0].name == "Sean"
    True
    >>> greedy_scheduled[False][0].name == "Al Roger"
    True
    >>> greedy_scheduled[True][1].name == "Jurena"
    True
    >>> b1.route == ["Earth", "Mars", "Venus"]
    True
    """
    _dmap: DistanceMap
    _passenger_priority: Callable[[Tuple, Tuple], bool]

    def __init__(self, _dmap: DistanceMap,
                 _passenger_priority: str):
        FleetScheduler.__init__(self)
        self._dmap = _dmap
        if _passenger_priority == 'travel_dist':
            self._passenger_priority = _priority_passenger_distance
        elif _passenger_priority == 'fare_bid':
            self._passenger_priority = _priority_passenger_bid
        else:
            self._passenger_priority = _priority_division

    def schedule(self, passengers: List[Passenger],
                 space_bikes: List[SpaceBike],
                 verbosity: int = 0) -> Dict[bool, List[Passenger]]:

        # result = {True: [], False: []}
        #
        # p_space_bike = PriorityQueue(_priority_spacebike)
        # for bike in space_bikes:
        #     if bike.max_capacity != 0:
        #         p_space_bike.add(bike)
        #
        # p_passengers = PriorityQueue(self._passenger_priority)
        # for passenger in passengers:
        #     p_passengers.add(passenger)

        # while not p_passengers.is_empty():
        result = {True: [], False: []}
        pq_passenger = PriorityQueue(self._passenger_priority)
        for passenger in passengers:
            pq_passenger.add((passenger, self._dmap))
        while not pq_passenger.is_empty():
            removed_p = pq_passenger.remove()
            if verbosity > 0:
                print(f"{removed_p[0].name} is selected as a candidate")
            pq_bike = PriorityQueue(_priority_spacebike)
            for bikes in space_bikes:
                pq_bike.add((bikes, removed_p[0], removed_p[1]))
            while not pq_bike.is_empty():
                removed_bike = pq_bike.remove()
                check = removed_bike[0].board(removed_p[0], removed_p[1])
                if check is True and verbosity > 0:
                    result[True].append(removed_p[0])
                    print(f"{removed_p[0].name} successfully "
                          f"boarded on the bike with an id of "
                          f"{removed_bike[0].id_}")
                elif check is True and verbosity == 0:
                    result[True].append(removed_p[0])
            if not removed_p[0].onboard:
                result[False].append(removed_p[0])
                if verbosity > 0:
                    print(f"{removed_p[0].name} could not board on any bike")
        return result


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['compare_algorithms'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'typing',
            'random', 'container', 'domain',
            'a2_space_bikes', 'a2_container', 'a2_distance_map'
        ],
        'max-attributes': 15,
        'disable': ['E1136']
    })
