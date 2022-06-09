from a2_space_bikes import SpaceFleet, SpaceBike, Passenger
from a2_container import PriorityQueue, _QueueNode
from a2_command_central import CommandCentral
from a2_distance_map import DistanceMap
from a2_fleet_scheduler import BogoScheduler, GreedyScheduler
import tempfile


def test_distance_map():
    dmap = DistanceMap()
    dmap.add_distance("Earth", "Mars", 0.1)
    dmap.add_distance("Earth", "Venus", 0.2)
    dmap.add_distance("Mars", "Venus", 0.5)

    assert dmap.distance("Earth", "Mars") == 0.1
    assert dmap.distance("Mars", "Earth") == 0.1

    assert dmap.distance("Earth", "Venus") == 0.2
    assert dmap.distance("Venus", "Earth") == 0.2

    assert dmap.distance("Venus", "Mars") == 0.5
    assert dmap.distance("Mars", "Venus") == 0.5


def test_non_existing_distance():
    dmap = DistanceMap()
    dmap.add_distance("Earth", "Mars", 0.1)
    dmap.add_distance("Earth", "Venus", 0.5)
    dmap.add_distance("Saturn", "Venus", 1.5)

    assert dmap.distance("Mars", "Venus") == -1.0
    assert dmap.distance("Earth", "Saturn") == -1.0


def test_different_vice_versa_distance():
    dmap = DistanceMap()
    dmap.add_distance("Earth", "Mars", 0.1)
    dmap.add_distance("Mars", "Earth", 2.0)
    dmap.add_distance("Saturn", "Venus", 1.5)
    dmap.add_distance("Venus", "Saturn", 0.7)

    assert dmap.distance("Saturn", "Venus") == 1.5
    assert dmap.distance("Venus", "Saturn") == 0.7
    assert dmap.distance("Earth", "Mars") == 0.1
    assert dmap.distance("Mars", "Earth") == 2.0


def test_complex_space_bikes_passenger():
    b1 = SpaceBike(1, "Atom Bike", 3, 3.5, 0.5)
    b2 = SpaceBike(2, "Nova Bike", 7, 7.0, 0.5)
    b3 = SpaceBike(3, "MC^2 Bike", 28, 30.5, 5.1)
    dmap = DistanceMap()
    dmap.add_distance("Earth", "Mars", 10.0)
    dmap.add_distance("Mars", "Venus", 15.0)
    dmap.add_distance("Venus", "Mars", 12.0)
    dmap.add_distance("Saturn", "Jupiter", 25.0)
    p1 = Passenger("Sean", 2.5, "Saturn", "Jupiter")
    p2 = Passenger("Jurena", 1.5, "Earth", "Mars")
    assert not b1.board(p1, dmap)
    # assert not p1.onboard
    assert not b2.board(p1, dmap)
    # assert not p1.onboard
    assert not b3.board(p1, dmap)
    # assert not p1.onboard
    b4 = SpaceBike(4, "MC^2 Bike", 28, 30.5, 1.2, "Saturn")
    assert b4.board(p1, dmap)
    # assert p1.onboard
    assert not b1.board(p2, dmap)
    # assert not p2.onboard
    assert b2.board(p2, dmap)
    # assert p2.onboard
    p3 = Passenger("Alvin", 1.7, "Mars", "Earth")
    assert not b3.board(p3, dmap)
    # assert not p3.onboard
    dmap.add_distance("Mars", "Earth", 0.5)
    assert b2.board(p3, dmap)
    # assert p3.onboard
    p4 = Passenger("Theodore", 2.5, "Earth", "Earth")
    assert b2.board(p4, dmap)
    # assert p4.onboard
    assert b2.route == ["Earth", "Mars", "Earth"]
    assert b4.route == ["Saturn", "Jupiter"]
    assert b1.route == ["Earth"]
    assert b3.route == ["Earth"]


def test_get_all_passenger_total_distance():
    b1 = SpaceBike(1, 'Nova Bike', 3, 8.0, 0.5)
    p1 = Passenger("Al Roger", 1.0, "Earth", "Mars")
    p2 = Passenger("Sean", 1.5, "Earth", "Uranus")
    p3 = Passenger("Brantford", 1.0, "Earth", "Saturn")
    dmap = DistanceMap()
    dmap.add_distance("Earth", "Mars", 8.0)
    dmap.add_distance("Mars", "Uranus", 8.0)
    dmap.add_distance("Uranus", "Saturn", 1.0)
    assert b1.board(p1, dmap)
    assert b1.board(p2, dmap)
    assert not b1.board(p3, dmap)
    assert b1.passengers == [p1, p2]
    # assert b1.total_distance(dmap) == 16.0


def test_space_bikes():
    sf = SpaceFleet()
    b1 = SpaceBike(100, "Nova Bike", 20, 8.0, 0.5)

    sf.add_space_bike(b1)

    dmap = DistanceMap()
    dmap.add_distance("Earth", "Mars", 0.1)
    dmap.add_distance("Earth", "Venus", 0.2)
    dmap.add_distance("Mars", "Venus", 0.5)

    # --------------------------------------------------
    #   Board a single passenger, starting in bike route
    # --------------------------------------------------

    p1 = Passenger("MaryAnn Jacobs", 1.0, "Earth", "Mars")
    assert b1.board(p1, dmap)
    assert sf.passenger_placements() == {
        100: ["MaryAnn Jacobs"]
    }
    assert sf.total_fare_collected() == 1.0
    assert sf.total_distance_travelled(dmap) == 0.1
    assert sf.vacant_seats() == 19

    # --------------------------------------------------
    #   Board a second passenger, starting in bike route
    # --------------------------------------------------
    p2 = Passenger("Richard LeFeuille", 1.0, "Earth", "Mars")
    assert b1.board(p2, dmap)
    assert sf.passenger_placements() == {
        100: ["MaryAnn Jacobs", "Richard LeFeuille"]
    }
    assert sf.total_fare_collected() == 2.0
    assert sf.total_distance_travelled(dmap) == 0.1
    assert sf.vacant_seats() == 18

    # --------------------------------------------------
    #   Try to board a third passenger, starting not in
    #   bike route
    # --------------------------------------------------
    p3 = Passenger("Howl Jenkins", 1.0, "Venus", "Mars")
    assert not b1.board(p3, dmap)
    assert sf.passenger_placements() == {
        100: ["MaryAnn Jacobs", "Richard LeFeuille"]
    }
    assert sf.total_fare_collected() == 2.0
    assert sf.total_distance_travelled(dmap) == 0.1
    assert sf.vacant_seats() == 18


def test_priority_queue():
    pq = PriorityQueue(int.__lt__)
    assert pq.is_empty()

    pq.add(1000)
    pq.add(10)
    pq.add(0)
    pq.add(200)
    pq.add(50)
    pq.add(60)

    assert isinstance(pq._first, _QueueNode)
    assert not pq.is_empty()

    val1 = pq.remove()
    val2 = pq.remove()
    val3 = pq.remove()
    val4 = pq.remove()
    val5 = pq.remove()
    val6 = pq.remove()

    assert val1 == 0
    assert val2 == 10
    assert val3 == 50
    assert val4 == 60
    assert val5 == 200
    assert val6 == 1000


#
#
# def _create_bogo_cc() -> CommandCentral:
#     config = {
#         "scheduler_type": "bogo",
#         "verbosity": 0,
#         "passenger_priority": "fare_per_dist",
#         "passenger_fname": "./data/testing/passengers_off_peak.txt",
#         "galaxy_fname": "./data/galaxy_data.txt",
#         "fleet_fname": "./data/testing/space_fleet_data.txt"
#     }
#
#     return CommandCentral(config)
#
#
# def _create_greedy_cc() -> CommandCentral:
#     config = {
#         "scheduler_type": "greedy",
#         "verbosity": 1,
#         "passenger_priority": "fare_bid",
#         "passenger_fname": "./data/testing/passengers_off_peak.txt",
#         "galaxy_fname": "./data/galaxy_data.txt",
#         "fleet_fname": "./data/testing/space_fleet_data.txt"
#     }
#
#     return CommandCentral(config)
#
#
# def test_command_central_attributes():
#     cc1 = _create_bogo_cc()
#
#     assert isinstance(cc1.scheduler, BogoScheduler)
#     assert cc1.fleet.num_space_bikes() == 34
#     assert cc1.verbosity == 0
#     assert isinstance(cc1.dmap, DistanceMap)
#     assert len(cc1.passengers) == 35
#
#     cc2 = _create_greedy_cc()
#
#     assert isinstance(cc2.scheduler, GreedyScheduler)
#     assert cc2.fleet.num_space_bikes() == 34
#     assert cc2.verbosity == 1
#     assert isinstance(cc2.dmap, DistanceMap)
#     assert len(cc2.passengers) == 35
#
#
# def test_fleet_bogo_scheduler():
#     fleet_str = """\
# Nova Bike
# ID_100\t20\t8.0\t0.5
#     """
#
#     tmp_fleet_file = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
#     tmp_fleet_file.write(fleet_str)
#
#     passenger_str = """\
# MaryAnn Jacobs
# BID: 1.0\tSOURCE: Earth\tDEST: Mars
# Canus Rex
# BID: 0.5\tSOURCE: Earth\tDEST: Mars
# Riley Adams
#  BID: 2.0\tSOURCE: Venus\tDEST: Earth
#     """
#
#     tmp_passenger_file = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
#     tmp_passenger_file.write(passenger_str)
#
#     galaxy_str = """\
# Earth\tMars\t0.1
# Earth\tVenus\t0.2
# Mars\tVenus\t0.5
#     """
#
#     tmp_galaxy_file = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
#     tmp_galaxy_file.write(galaxy_str)
#
#     config = {
#         "scheduler_type": "bogo",
#         "verbosity": 0,
#         "passenger_fname": f"{tmp_passenger_file.name}",
#         "galaxy_fname": f"{tmp_galaxy_file.name}",
#         "fleet_fname": f"{tmp_fleet_file.name}"
#     }
#
#     tmp_galaxy_file.close()
#     tmp_fleet_file.close()
#     tmp_passenger_file.close()
#
#     cc = CommandCentral(config)
#
#     # run the scheduler
#     cc.run(report=False)
#
#     passenger_placements = cc.fleet.passenger_placements()
#
#     assert "MaryAnn Jacobs" in passenger_placements[100]
#     assert "Canus Rex" in passenger_placements[100]
#     assert "Riley Adams" not in passenger_placements[100]
#
#
# def test_fleet_greedy_scheduler():
#     fleet_str = """\
#     Nova Bike
#     ID_100\t20\t8.0\t0.5
#         """
#
#     tmp_fleet_file = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
#     tmp_fleet_file.write(fleet_str)
#
#     passenger_str = """\
#     MaryAnn Jacobs
#     BID: 1.0\tSOURCE: Earth\tDEST: Mars
#     Canus Rex
#     BID: 0.5\tSOURCE: Earth\tDEST: Mars
#     Riley Adams
#      BID: 2.0\tSOURCE: Venus\tDEST: Earth
#         """
#
#     tmp_passenger_file = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
#     tmp_passenger_file.write(passenger_str)
#
#     galaxy_str = """\
#     Earth\tMars\t0.1
#     Earth\tVenus\t0.2
#     Mars\tVenus\t0.5
#         """
#
#     tmp_galaxy_file = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
#     tmp_galaxy_file.write(galaxy_str)
#
#     config = {
#         "scheduler_type": "greedy",
#         "verbosity": 0,
#         "passenger_priority": "fare_bid",
#         "passenger_fname": f"{tmp_passenger_file.name}",
#         "galaxy_fname": f"{tmp_galaxy_file.name}",
#         "fleet_fname": f"{tmp_fleet_file.name}"
#     }
#
#     tmp_galaxy_file.close()
#     tmp_fleet_file.close()
#     tmp_passenger_file.close()
#
#     cc = CommandCentral(config)
#
#     # run the scheduler
#     cc.run(report=False)
#
#     passenger_placements = cc.fleet.passenger_placements()
#     assert passenger_placements[100] == ["MaryAnn Jacobs", "Canus Rex"]


if __name__ == "__main__":
    import pytest

    pytest.main(['starter_tests_a2.py'])
