import sys
import os
sys.path.append(os.path.dirname(__file__))

from base_test import BasicTest, BasicUtil
from test_building import BuildingUtil
from test_room import RoomUtil
from test_seat import SeatUtil

class SeatSearchTest(BasicTest):
    def setUp(self):
        self.building_util = BuildingUtil()
        self.room_util = RoomUtil()
        self.seat_util = SeatUtil()

    def test_search_seat_by_availability(self):
        self.building_util.create_building()
        self.room_util.create_room()
        self.seat_util.create_seat()
        response = self.seat_util.app.get("/api/seat/search?available=true")
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("seats", data)

    def test_search_seat_near_window(self):
        self.building_util.create_building()
        self.room_util.create_room()
        self.seat_util.create_seat(near_window=True)
        response = self.seat_util.app.get("/api/seat/search?near_window=true")
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("seats", data)

    def test_search_seat_near_fixed_socket(self):
        self.building_util.create_building()
        self.room_util.create_room()
        self.seat_util.create_seat(near_fixed_socket=True)
        response = self.seat_util.app.get("/api/seat/search?near_fixed_socket=true")
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("seats", data)

    def test_search_seat_near_movable_socket(self):
        self.building_util.create_building()
        self.room_util.create_room()
        self.seat_util.create_seat(near_movable_socket=True)
        response = self.seat_util.app.get("/api/seat/search?near_movable_socket=true")
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("seats", data)

    def test_search_seat_by_all_parameters(self):
        self.building_util.create_building()
        self.room_util.create_room()
        self.seat_util.create_seat(near_fixed_socket=True, near_movable_socket=True, near_window=True)
        response = self.seat_util.app.get("/api/seat/search?available=true&near_fixed_socket=true&near_movable_socket=true&near_window=true")
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("seats", data)
        
    def test_search_seat_no_result(self):
        response = self.seat_util.app.get("/api/seat/search")
        self.assertEqual(response.status_code, 404)
        data = response.json
        self.assertIn("message", data)
