"""Assignment 2 - Command Central [Task 5]

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

This module contains class CommandCentral.  It creates the appropriate
scheduler instance according to a configuration dictionary, then
runs the scheduler, generates statistics, and (optionally) reports the
statistics.

This module is responsible for all the reading of data from the data files.
"""

from typing import Dict, List, Union, Optional
from a2_fleet_scheduler import BogoScheduler, GreedyScheduler, FleetScheduler
from a2_space_bikes import SpaceBike, SpaceFleet, Passenger
from a2_distance_map import DistanceMap


def load_fleet_data(fleet_fname: str) -> SpaceFleet:
    """Read SpaceFleet data from <fleet_fname> and return
    an instance of SpaceFleet with all of the SpaceBikes found
    in the <fleet_fname> file.

    Precondition: <fleet_fname> is the path to a file containing fleet data in
                  the form specified in the A2 handout.
    """
    f = open(fleet_fname)
    sf = SpaceFleet()
    line = f.readline()
    while line.strip() != "":
        name = line.strip()
        contents = [item.strip()
                    for item in f.readline().strip().split('\t')]

        id_, max_passengers, fuel_capacity, fuel_usage_rate = \
            contents[0], contents[1], \
            contents[2], contents[3]

        space_bike = SpaceBike(int(id_.split("_")[-1].strip()), name,
                               int(max_passengers), float(fuel_capacity),
                               float(fuel_usage_rate))
        sf.add_space_bike(space_bike)
        line = f.readline()
    f.close()
    return sf


def load_galaxy_data(galaxy_fname: str) -> DistanceMap:
    """Read Galaxy data from <galaxy_fname> and return
    an instance of DistanceMap that records the inter-galactic
    distances.

    Precondition: <galaxy_fname> is the path to a file containing galaxy
                  data in the form specified in the A2 handout.
    """

    f = open(galaxy_fname)

    dmap = DistanceMap()
    line = f.readline()
    while line.strip() != "":
        contents = [item.strip() for item in line.split('\t')]
        loc1 = contents[0]
        loc2 = contents[1]

        c1 = float(contents[2])
        next_line = f.readline()
        if next_line.strip() != "":
            next_contents = [items.strip() for items in next_line.split('\t')]
            loc11 = next_contents[0]
            loc22 = next_contents[1]
            if loc11 == loc2 and loc22 == loc1:
                c2 = float(next_contents[2])
                dmap.add_distance(loc1, loc2, c1)
                dmap.add_distance(loc2, loc1, c2)
            else:
                c2 = float(next_contents[2])
                dmap.add_distance(loc1, loc2, c1)
                dmap.add_distance(loc11, loc22, c2)
        # process the next line
        line = f.readline()
    f.close()

    return dmap


def load_passenger_data(passenger_fname: str) -> List[Passenger]:
    """Read Passenger data from <passenger_fname> and return
    a List of Passengers.

    Precondition: <passenger_fname> is the path to a file containing
                  passenger data in the form specified in the A2 handout.
    """
    f = open(passenger_fname)

    passenger = []

    line = f.readline()
    while line.strip() != "":
        name = line.strip()

        contents = [item.strip()
                    for item in f.readline().strip().split('\t')]

        bid = float(contents[0].split(":")[-1].strip())
        source = contents[1].split(":")[-1].strip()
        dest = contents[2].split(":")[-1].strip()

        passenger.append(Passenger(name, bid, source, dest))
        line = f.readline()

    f.close()
    return passenger


class CommandCentral:
    """A command central which runs a particular scheduler with a set of
    configurations, computes the results of the scheduler, and reports
    these results.

    This is achieved through the following steps:

    1. Read in all data from necessary files, and create corresponding objects.
    2. Run a scheduling algorithm to assign passengers to space bikes.
    3. Compute statistics showing how good the assignment of passengers to bikes
    is.
    4. Report the statistics from the scheduler.

    === Public Attributes ===
    verbosity:
      If <verbosity> is non-zero, print step-by-step details regarding the
      scheduling algorithm as it runs.
    scheduler:
      The scheduler to run.
    passengers:
      The passengers to schedule onboard the space bikes.
    fleet:
      The SpaceBikes that passengers are scheduled onboard.
    dmap:
      The distances between locations.

    === Private Attributes ===
    _stats:
      A dictionary of statistics. <_stats>'s value is undefined until
      <self>._compute_stats is called, at which point it contains keys and
      values as described in the A2 handout.
    _unboarded:
      A list of passengers. <_unboarded>'s value is undefined until <self>.run
      is called, at which point it contains the list of passengers that could
      not be scheduled onboard any bikes.

    === Representation Invariants ===
    - <fleet> contains at least one space bike.
    - <dmap> contains all of the distances required to compute the length of
      any possible route for the space bikes in <fleet> for any source and
      destination passengers can request travel between.
    """
    verbosity: int
    passenger_priority: Optional[str]
    passengers: List[Passenger]
    fleet: SpaceFleet
    dmap: DistanceMap
    scheduler: FleetScheduler
    _unboarded: List[Passenger]
    _stats: Dict[str, Union[int, float]]

    def __init__(
            self,
            config: Dict[str, Union[str, int]]
    ) -> None:
        self.verbosity = config['verbosity']

        if "passenger_priority" in config:
            self.passenger_priority = config["passenger_priority"]
        else:
            self.passenger_priority = None
        self.passengers = load_passenger_data(config["passenger_fname"])
        self.fleet = load_fleet_data(config["fleet_fname"])
        self.dmap = load_galaxy_data(config["galaxy_fname"])

        self._stats = {}
        self._unboarded = []

        if config['scheduler_type'] == 'bogo':
            self.scheduler = BogoScheduler(self.dmap)
        else:
            self.scheduler = GreedyScheduler(self.dmap, self.passenger_priority)

    def run(self, report: bool = False) -> Dict[str, Union[int, float]]:
        """Run the scheduler and return statistics on the outcome.

        The return value is a dictionary with keys and values are as specified
        in the A2 handout (Task 5).

        If <report> is True, print a report on the statistics from this
        experiment.

        If <self.verbosity> is non-zero, print step-by-step details
        regarding the scheduling algorithm as it runs.
        """

        # This method has been completed for you.
        # DO NOT modify it.

        passengers = self.scheduler.schedule(
            self.passengers, self.fleet.bikes, self.verbosity
        )

        unboarded = passengers[False]
        boarded = passengers[True]

        total_boarded = len(boarded)

        # try to keep scheduling un-boarded passengers
        s = ""
        if report:
            if isinstance(self.scheduler, GreedyScheduler):
                s = "GreedyScheduler"
            else:
                s = "BogoScheduler"
            print(f"---------- Now running {s} -----------")

        i = 0
        while len(boarded) != 0:
            # so as long as passengers continue to be boarded
            if report:
                print(f"ITERATION {i}:\t {total_boarded} "
                      f"BOARDED \t {len(unboarded)} UNBOARDED")
            passengers = self.scheduler.schedule(
                unboarded, self.fleet.bikes, self.verbosity
            )
            unboarded = passengers[False]
            boarded = passengers[True]
            total_boarded += len(boarded)

            i += 1

        self._unboarded = unboarded

        self._compute_stats()
        if report:
            print(f"---- {s} complete in {i} iterations ----")
            print("!!--- Now printing report ---!!")
            self._print_report()
            print("!!--- End of report ---!!")

        return self._stats

    def _compute_stats(self) -> None:
        """Compute the statistics, and store in <self>.stats.
        Keys and values are as specified in the A2 handout under the
        section Task 5.

        Precondition: <self>._run has already been called.
        """
        self._stats = {
            'num_bikes': self.fleet.num_space_bikes(),
            'num_empty_bikes': (self.fleet.num_space_bikes() -
                                self.fleet.num_nonempty_bikes()),
            'average_fill_percent': self.fleet.average_fill_percent(),
            'average_distance_travelled':
                self.fleet.average_distance_travelled(self.dmap),
            'vacant_seats': self.fleet.vacant_seats(),
            'total_fare_collected': self.fleet.total_fare_collected(),
            'deployment_cost': self.fleet.total_deployment_cost(self.dmap),
            'profit': (self.fleet.total_fare_collected() -
                       self.fleet.total_deployment_cost(self.dmap))
        }

    def _print_report(self) -> None:
        """Report on the statistics stored in <self>._statistics

        This method is *only* for debugging purposes for your benefit, so
        the content and format of the report is your choice; we
        will not call your run method with <report> set to True.

        Precondition: <self>._compute_stats has already been called.
        """

        print(f"There are {self._stats['num_bikes']} bikes in total \n"
              f"There are {self._stats['num_empty_bikes']} empty bikes \n"
              f"The average fill percent is "
              f"{self._stats['average_fill_percent']} % \n"
              f"The average distance travelled is "
              f"{self._stats['average_distance_travelled']} \n"
              f"There are {self._stats['vacant_seats']} vacant seats\n"
              f"We have collected {self._stats['total_fare_collected']} "
              f"in total \n"
              f"We have spent {self._stats['deployment_cost']} \n"
              f"We have earned {self._stats['profit']}.")


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['load_fleet_data', 'load_galaxy_data',
                       'load_passenger_data', 'run'
                                              '_print_report'],
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'a2_fleet_scheduler',
                                   'a2_space_bikes',
                                   'a2_distance_map'],
        'disable': ['E1136', 'E9998'],
        'max-attributes': 15,
    })

    # ------------------------------------------------------------------------
    # Change the following config to test your schedulers on different
    # parameters
    # ------------------------------------------------------------------------

    config_base = {
        "scheduler_type": "bogo",
        "verbosity": 0,
        "passenger_priority": "fare_per_dist",
        "passenger_fname": "./data/testing/passengers_off_peak.txt",
        "galaxy_fname": "./data/galaxy_data.txt",
        "fleet_fname": "./data/testing/space_fleet_data.txt"
    }

    cc = CommandCentral(config_base)
    cc.run(report=True)
