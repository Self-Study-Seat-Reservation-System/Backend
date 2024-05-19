import sys
import os
sys.path.append(os.path.dirname(__file__))

from base_test import BasicTest, BasicUtil
from test_room import RoomUtil
from unittest.mock import patch
from utils.resource_checker import ResourceChecker

class SeatUtil(BasicUtil):
    def create_seat(self, room_id=1, near_fixed_socket=False, near_movable_socket=False, near_window=False):
        data = {
            "room_id": room_id,
            "near_fixed_socket": near_fixed_socket,
            "near_movable_socket": near_movable_socket,
            "near_window": near_window
        }

        response = self.app.post("/api/seat", headers=self.headers, json=data)
        return response

    def update_seat(self, seat_id, data):
        response = self.app.put(f"/api/seat/{seat_id}",  headers=self.headers, json=data)
        return response
    
    def delete_seat(self, seat_id):
        response = self.app.delete(f"/api/seat/{seat_id}")
        return response


class SeatTest(BasicTest):
    def setUp(self):
        self.seat_util = SeatUtil()
        self.room_util = RoomUtil()
        self.patcher = patch.object(ResourceChecker, 'check_building_available')
        self.mock_check = self.patcher.start()
        self.mock_check.return_value = ({"message": "Building is available."}, 200)

    def tearDown(self):
        self.patcher.stop()
    
    def test_create_seat_successfully(self):
        self.room_util.create_room()
        response = self.seat_util.create_seat()
        self.assertEqual(response.status_code, 201)

    def test_create_seat_without_room(self):
        response = self.seat_util.create_seat()
        self.assertEqual(response.status_code, 404)

    def test_create_seat_with_deprecated_room(self):
        self.room_util.create_room()
        self.room_util.delete_room(1)
        response = self.seat_util.create_seat()
        self.assertEqual(response.status_code, 400)

    def test_delete_seat_successfully(self):
        self.room_util.create_room()
        self.seat_util.create_seat()
        response = self.seat_util.delete_seat(1)
        self.assertEqual(response.status_code, 200)

    def test_delete_seat_without_seat(self):
        response = self.seat_util.delete_seat(1)
        self.assertEqual(response.status_code, 404)

    def test_update_seat_successfully(self):
        self.room_util.create_room()
        self.seat_util.create_seat()
        data = {
            "near_fixed_socket": True,
            "near_movable_socket": False,
            "near_window": True,
            "deprecated": False
        }
        response = self.seat_util.update_seat(1, data)
        self.assertEqual(response.status_code, 200)
        data = {
            "near_fixed_socket": False
        }
        response = self.seat_util.update_seat(1, data)
        self.assertEqual(response.status_code, 200)