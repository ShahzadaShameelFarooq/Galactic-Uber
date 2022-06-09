"""Assignment 2 - SpaceBikes, Passengers, and SpaceFleets.

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

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 the Department of Computer Science,
University of Toronto

===== Module Description =====

This module contains the Passenger, SpaceBike, and SpaceFleet
classes.
"""

from typing import List, Dict
from a2_distance_map import DistanceMap

DEFAULT_STARTING_LOC = 'Earth'
FUEL_COST_PER_UNIT = 0.75


class Passenger:
    """

    """
    name: str
    bid: float
    source: str
    destination: str
    starting_loc: str
    onboard: bool

    def __init__(self, name: str, bid: float,
                 source: str, destination: str) -> None:
        """

        """
        self.name = name
        self.bid = bid
        self.source = source
        self.destination = destination
        self.onboard = False


class SpaceBike:
    """

    """
    id_number: int
    type_bike: str
    max_capacity: int
    fuel_capacity: float
    fuel_usage_rate: float
    route: List
    starting_loc: str
    initial_capacity: int
    passengers = List[str]

    def __init__(self, id_number: int, type_bike: str, max_capacity: int,
                 fuel_capacity: float, fuel_usage_rate: float,
                 starting_loc: str = DEFAULT_STARTING_LOC) -> None:
        """

        """
        self.id_number = id_number
        self.type_bike = type_bike
        self.max_capacity = max_capacity
        self.fuel_capacity = fuel_capacity
        self.fuel_usage_rate = fuel_usage_rate
        self.route = [starting_loc]
        self.starting_loc = DEFAULT_STARTING_LOC
        self.initial_capacity = max_capacity
        self.passengers = []

    def board(self, p: Passenger, d: DistanceMap) -> bool:
        """

        """
        # dist = d.distance(p.source, p.destination)
        # req_fuel = dist + self.fuel_usage_rate
        #
        # if self.max_capacity > 0 and (p.source in self.route or (
        #         p.source and p.destination in self.route) and
        #                               self.fuel_capacity >= req_fuel):
        #
        #     self.max_capacity = self.max_capacity - 1
        #     self.fuel_capacity = self.fuel_capacity - req_fuel
        #
        #     # if p.source + p.destination not in self.route:
        #     #     #     self.route = p.source + p.destination
        #     #     # else:
        #     #     #     self.route = self.route + p.destination
        #     #     self.route.append(p.source + p.destination)
        #     if p.destination not in self.route:
        #         self.route.append(p.destination)
        #     self.passengers.append(p)
        #     return True
        # else:
        #     return False

        dist = d.distance(p.source, p.destination)
        if self.max_capacity > 0 and p.source in self.route:
            if p.destination in self.route and self.route.index(p.source) \
                    < self.route.index(p.destination):
                self.max_capacity = self.max_capacity - 1
                self.passengers.append(p)
                p.onboard = True
                return True

            elif self.max_capacity > 0 and p.source == p.destination and p.source in self.route:
                self.max_capacity = self.max_capacity - 1
                self.passengers.append(p)
                p.onboard = True
                return True

            else:
                if dist != -1:
                    req_fuel = dist * self.fuel_usage_rate
                    if self.fuel_capacity >= req_fuel:
                        self.fuel_capacity = self.fuel_capacity - req_fuel
                        self.max_capacity = self.max_capacity - 1
                        d = self.route
                        self.route.append(p.destination)
                        self.passengers.append(p)
                        s = self.route
                        p.onboard = True
                        return True
                return False

        else:
            return False


class SpaceFleet:
    """A Fleet of SpaceBikes for intergalactic travel.

    === Public Attributes ===
    bikes:
      List of all SpaceBike objects in this SpaceFleet

    """
    bikes: List[SpaceBike]

    def __init__(self) -> None:
        """Create a SpaceFleet with no bikes.

        >>> sf = SpaceFleet()
        >>> sf.num_space_bikes()
        0
        """

        self.bikes = []

    def add_space_bike(self, space_bike: SpaceBike) -> None:
        """Add space_bike to this SpaceFleet.

        Precondition: No other space_bike with the same ID as
        space_bike has already been added to this Fleet.

        >>> sf = SpaceFleet()
        >>> sb = SpaceBike(198761, 'Nova Bike', 20, 8.0, 0.5)
        >>> sf.add_space_bike(sb)
        >>> sf.num_space_bikes()
        1
        """

        self.bikes.append(space_bike)

    def num_space_bikes(self) -> int:
        """Return the number of bikes in this SpaceFleet.

        >>> sf = SpaceFleet()
        >>> sf.num_space_bikes()
        0
        >>> sb = SpaceBike(198761, 'Nova Bike', 20, 8.0, 0.5)
        >>> sf.add_space_bike(sb)
        >>> sf.num_space_bikes()
        1
        """
        return len(self.bikes)

    def num_nonempty_bikes(self) -> int:
        """Return the number of SpaceBikes that are not empty.

        >>> sf = SpaceFleet()
        >>> b1 = SpaceBike(198161, 'Nova Bike', 20, 8.0, 0.5)
        >>> b2 = SpaceBike(198761, 'Nova Bike', 20, 8.0, 0.5)
        >>> b3 = SpaceBike(198561, 'Nova Bike', 20, 8.0, 0.5)
        >>> sf.add_space_bike(b1)
        >>> sf.add_space_bike(b2)
        >>> sf.add_space_bike(b3)
        >>> p1 = Passenger("Al Roger", 1.0, "Earth", "Mars")
        >>> dmap = DistanceMap()
        >>> dmap.add_distance("Earth", "Mars", 0.4)
        >>> b1.board(p1, dmap)
        True
        >>> sf.num_nonempty_bikes()
        1
        >>> p2 = Passenger("Al Frank", 1.0, "Earth", "Mars")
        >>> b2.board(p2, dmap)
        True
        >>> sf.num_nonempty_bikes()
        2
        """
        t = 0
        for b in self.bikes:
            if b.max_capacity != b.initial_capacity:
                t = t + 1
        return t

    def passenger_placements(self) -> Dict[int, List[str]]:
        """Return a dictionary in which each key is the ID of a SpaceBike
        in this fleet and its value is a list of the passengers on board
        the SpaceBike, in the order that they boarded.

        >>> sf = SpaceFleet()
        >>> b1 = SpaceBike(198161, 'Nova Bike', 20, 8.0, 0.5)
        >>> b2 = SpaceBike(198761, 'Nova Bike', 20, 8.0, 0.5)
        >>> b3 = SpaceBike(198561, 'Nova Bike', 20, 8.0, 0.5)
        >>> sf.add_space_bike(b1)
        >>> sf.add_space_bike(b2)
        >>> sf.add_space_bike(b3)
        >>> p1 = Passenger("Al Roger", 1.0, "Earth", "Mars")
        >>> dmap = DistanceMap()
        >>> dmap.add_distance("Earth", "Mars", 0.4)
        >>> b1.board(p1, dmap)
        True
        >>> p2 = Passenger("Al Frank", 1.0, "Earth", "Mars")
        >>> b2.board(p2, dmap)
        True
        >>> p3 = Passenger("Anne Rose", 1.0, "Earth", "Mars")
        >>> b2.board(p3, dmap)
        True
        >>> sf.passenger_placements() == {
        ...     198161: ["Al Roger"],
        ...     198761: ["Al Frank", "Anne Rose"],
        ...     198561: []
        ... }
        True
        """

        result = {}
        for bike in self.bikes:
            result[bike.id_number] = []
            for passenger in bike.passengers:
                result[bike.id_number].append(passenger.name)

        return result

    def vacant_seats(self) -> int:
        """Return the total number of seats available across all *non-empty*
        SpaceBikes in the SpaceFleet.

        If there are no non-empty SpaceBikes in the SpaceFleet, return 0.

        >>> sf = SpaceFleet()
        >>> b1 = SpaceBike(198161, 'Nova Bike', 20, 8.0, 0.5)
        >>> b2 = SpaceBike(198761, 'Nova Bike', 20, 8.0, 0.5)
        >>> b3 = SpaceBike(198561, 'Nova Bike', 20, 8.0, 0.5)
        >>> sf.add_space_bike(b1)
        >>> sf.add_space_bike(b2)
        >>> sf.add_space_bike(b3)
        >>> p1 = Passenger("Al Roger", 1.0, "Earth", "Mars")
        >>> dmap = DistanceMap()
        >>> dmap.add_distance("Earth", "Mars", 0.4)
        >>> b1.board(p1, dmap)
        True
        >>> p2 = Passenger("Al Frank", 1.0, "Earth", "Mars")
        >>> b2.board(p2, dmap)
        True
        >>> p3 = Passenger("Anne Rose", 1.0, "Earth", "Mars")
        >>> b2.board(p3, dmap)
        True
        >>> sf.vacant_seats()
        37

        """
        s = 0
        if self.num_nonempty_bikes() == 0:
            return 0
        else:
            for b in self.bikes:
                if b.max_capacity != b.initial_capacity:
                    s = s + b.max_capacity
            return s

    def total_fare_collected(self) -> float:
        """Return the total amount of fare collected from all
        Passengers on board all SpaceBikes in this SpaceFleet.

        >>> sf = SpaceFleet()
        >>> b1 = SpaceBike(198161, 'Nova Bike', 20, 8.0, 0.5)
        >>> b2 = SpaceBike(198761, 'Nova Bike', 20, 8.0, 0.5)
        >>> b3 = SpaceBike(198561, 'Nova Bike', 20, 8.0, 0.5)
        >>> sf.add_space_bike(b1)
        >>> sf.add_space_bike(b2)
        >>> sf.add_space_bike(b3)
        >>> p1 = Passenger("Al Roger", 1.0, "Earth", "Mars")
        >>> dmap = DistanceMap()
        >>> dmap.add_distance("Earth", "Mars", 0.4)
        >>> b1.board(p1, dmap)
        True
        >>> p2 = Passenger("Al Frank", 1.0, "Earth", "Mars")
        >>> b2.board(p2, dmap)
        True
        >>> p3 = Passenger("Anne Rose", 1.0, "Earth", "Mars")
        >>> b2.board(p3, dmap)
        True
        >>> sf.total_fare_collected() == 3.0
        True
        """

        total = 0
        for bike in self.bikes:
            if bike.passengers:
                for passenger in bike.passengers:
                    total = total + passenger.bid
            else:
                total = total
        return total

    def total_distance_travelled(self, dmap: DistanceMap) -> float:
        """Return the total distance travelled across all SpaceBikes
        in this SpaceFleet.

        The distance travelled is calculated for each SpaceBike according
        to their route and <dmap>.

        >>> sf = SpaceFleet()
        >>> b1 = SpaceBike(198161, 'Nova Bike', 20, 8.0, 0.5)
        >>> b2 = SpaceBike(198761, 'Nova Bike', 20, 8.0, 0.5)
        >>> b3 = SpaceBike(198561, 'Nova Bike', 20, 8.0, 0.5)
        >>> sf.add_space_bike(b1)
        >>> sf.add_space_bike(b2)
        >>> sf.add_space_bike(b3)
        >>> p1 = Passenger("Al Roger", 1.0, "Earth", "Mars")
        >>> dmap = DistanceMap()
        >>> dmap.add_distance("Earth", "Mars", 0.4)
        >>> b1.board(p1, dmap)
        True
        >>> p2 = Passenger("Al Frank", 1.0, "Earth", "Mars")
        >>> b2.board(p2, dmap)
        True
        >>> p3 = Passenger("Anne Rose", 1.0, "Earth", "Mars")
        >>> b2.board(p3, dmap)
        True
        >>> sf.total_distance_travelled(dmap) == 0.8
        True

        """
        t = 0
        for bike in self.bikes:
            for i in range(0, len(bike.route) - 1):
                # s = bike.route
                t = t + dmap.distance(bike.route[i], bike.route[i + 1])
                # print(bike.route[i])
                # print(bike.route[i + 1])
        return t

    def _total_passenger_count(self) -> int:
        """Return the total number of passengers boarded
        across all SpaceBikes in this SpaceFleet.

        >>> sf = SpaceFleet()
        >>> b1 = SpaceBike(198161, 'Nova Bike', 20, 8.0, 0.5)
        >>> b2 = SpaceBike(198761, 'Nova Bike', 20, 8.0, 0.5)
        >>> b3 = SpaceBike(198561, 'Nova Bike', 20, 8.0, 0.5)
        >>> sf.add_space_bike(b1)
        >>> sf.add_space_bike(b2)
        >>> sf.add_space_bike(b3)
        >>> p1 = Passenger("Al Roger", 1.0, "Earth", "Mars")
        >>> dmap = DistanceMap()
        >>> dmap.add_distance("Earth", "Mars", 0.4)
        >>> b1.board(p1, dmap)
        True
        >>> p2 = Passenger("Al Frank", 1.0, "Earth", "Mars")
        >>> b2.board(p2, dmap)
        True
        >>> p3 = Passenger("Anne Rose", 1.0, "Earth", "Mars")
        >>> b2.board(p3, dmap)
        True
        >>> sf._total_passenger_count()
        3
        """

        total = 0
        for bike in self.bikes:
            total = total + (bike.initial_capacity - bike.max_capacity)
        return total

    def average_fill_percent(self) -> float:
        """Return the average fill percent across all SpaceBikes in
        this SpaceFleet.

        Precondition:
        - there is at least one SpaceBike in the SpaceFleet.

        >>> sf = SpaceFleet()
        >>> b1 = SpaceBike(198161, 'Nova Bike', 20, 8.0, 0.5)
        >>> b2 = SpaceBike(198761, 'Nova Bike', 20, 8.0, 0.5)
        >>> b3 = SpaceBike(198561, 'Nova Bike', 20, 8.0, 0.5)
        >>> sf.add_space_bike(b1)
        >>> sf.add_space_bike(b2)
        >>> sf.add_space_bike(b3)
        >>> p1 = Passenger("Al Roger", 1.0, "Earth", "Mars")
        >>> dmap = DistanceMap()
        >>> dmap.add_distance("Earth", "Mars", 0.4)
        >>> b1.board(p1, dmap)
        True
        >>> p2 = Passenger("Al Frank", 1.0, "Earth", "Mars")
        >>> b2.board(p2, dmap)
        True
        >>> p3 = Passenger("Anne Rose", 1.0, "Earth", "Mars")
        >>> b2.board(p3, dmap)
        True
        >>> # b1: 1/20, b2: 2/20, b3: 0/20
        >>> # 100 * (1/20 + 2/20 + 0/20) / 3 = 5
        >>> eps = 0.0001  # floating point error tolerance
        >>> abs(sf.average_fill_percent() - 5) < eps
        True

        """
        t = 0
        for bike in self.bikes:
            t = t + ((bike.initial_capacity -
                      bike.max_capacity) / bike.initial_capacity)
        return 100 * (t / len(self.bikes))

    def average_distance_travelled(self, dmap: DistanceMap) -> float:
        """Return the average distance travelled across all **non-empty**
        SpaceBikes in this SpaceFleet.

        The average distance travelled is defined as the total distance
        travelled divided by the number of **non-empty** SpaceBikes in the
        SpaceFleet.

        >>> sf = SpaceFleet()
        >>> b1 = SpaceBike(198161, 'Nova Bike', 20, 8.0, 0.5)
        >>> b2 = SpaceBike(198761, 'Nova Bike', 20, 8.0, 0.5)
        >>> b3 = SpaceBike(198561, 'Nova Bike', 20, 8.0, 0.5)
        >>> sf.add_space_bike(b1)
        >>> sf.add_space_bike(b2)
        >>> sf.add_space_bike(b3)
        >>> p1 = Passenger("Al Roger", 1.0, "Earth", "Mars")
        >>> dmap = DistanceMap()
        >>> dmap.add_distance("Earth", "Mars", 0.4)
        >>> b1.board(p1, dmap)
        True
        >>> p2 = Passenger("Al Frank", 1.0, "Earth", "Mars")
        >>> b2.board(p2, dmap)
        True
        >>> p3 = Passenger("Anne Rose", 1.0, "Earth", "Mars")
        >>> b2.board(p3, dmap)
        True
        >>> sf.average_distance_travelled(dmap) # b3 is empty, do not include
        0.4
        """

        total_d = self.total_distance_travelled(dmap)
        b = []
        for bike in self.bikes:
            if bike.max_capacity != bike.initial_capacity:
                b.append(bike)
        if len(b) == 0:
            return 0
        return total_d / len(b)

    def total_deployment_cost(self, dmap: DistanceMap) -> float:
        """Return the total deployment cost for deploying all **non-empty**
        SpaceBikes in the fleet.

        The deployment cost is defined as the sum of the base cost of
        operation (see A2 handout) and the total fuel cost. The total fuel
        cost for a single space bike is the total fuel expended by its route,
        multiplied by the FUEL_COST_PER_UNIT constant.

        >>> sf = SpaceFleet()
        >>> b1 = SpaceBike(198161, 'Nova Bike', 20, 8.0, 0.5)
        >>> b2 = SpaceBike(198761, 'Nova Bike', 20, 8.0, 0.5)
        >>> b3 = SpaceBike(198561, 'Nova Bike', 20, 8.0, 0.5)
        >>> sf.add_space_bike(b1)
        >>> sf.add_space_bike(b2)
        >>> sf.add_space_bike(b3)
        >>> p1 = Passenger("Al Roger", 1.0, "Earth", "Mars")
        >>> dmap = DistanceMap()
        >>> dmap.add_distance("Earth", "Mars", 0.4)
        >>> b1.board(p1, dmap)
        True
        >>> p2 = Passenger("Al Frank", 1.0, "Earth", "Mars")
        >>> b2.board(p2, dmap)
        True
        >>> p3 = Passenger("Anne Rose", 1.0, "Earth", "Mars")
        >>> b2.board(p3, dmap)
        True
        >>> sf.total_deployment_cost(dmap)
        5.1
        """

        non_empty_bikes = []
        for bike in self.bikes:
            if bike.max_capacity != bike.initial_capacity:
                non_empty_bikes.append(bike)
        if len(non_empty_bikes) == 0:
            return 0
        else:
            t = 0
            for bike in non_empty_bikes:
                one = 0
                for i in range(0, len(bike.route) - 1):
                    fuel_use = bike.fuel_usage_rate * dmap.distance(
                        bike.route[i], bike.route[i + 1])
                    one = one + (fuel_use * FUEL_COST_PER_UNIT)
                    if bike.type_bike == 'Atom Bike':
                        one = one + 1.2
                    elif bike.type_bike == 'Nova Bike':
                        one = one + 2.4
                    else:
                        one = one + 10.1
                t = t + one
            return t


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'typing', 'a2_distance_map'
        ],
        'max-attributes': 15,
        'max-args': 15,
        'disable': ['E1136']
    })

    import doctest

    doctest.testmod()
