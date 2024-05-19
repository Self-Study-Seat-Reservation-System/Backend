import sys
import os
sys.path.append(os.path.dirname(__file__))

from base_test import BasicTest, BasicUtil
from test_room import RoomUtil
from unittest.mock import patch
from utils.resource_checker import ResourceChecker

class SeatUtil(BasicUtil):
    def create_seat(self, room_id=1, near_fixed_socket=False, near_movable_socket=False, near_window=False):
        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "room_id": room_id,
            "near_fixed_socket": near_fixed_socket,
            "near_movable_socket": near_movable_socket,
            "near_window": near_window
        }

        response = self.app.post("/api/seat", headers=headers, json=data)
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