import sys
import os
sys.path.append(os.path.dirname(__file__))

from base_test import BasicTest, BasicUtil
from datetime import datetime
from test_room import RoomUtil
from test_seat import SeatUtil
from test_student import StudentUtil
from unittest.mock import patch
from utils.resource_checker import ResourceChecker
from utils.time import TimeService

class ReservationUtil(BasicUtil):
    def create_reservation(self, user_id=1, room_id=1, seat_id=1, 
            start_time="2024-05-20 15:00:00", end_time="2024-05-20 16:00:00"):
        data = {
            "user_id": user_id,
            "room_id": room_id,
            "seat_id": seat_id,
            "start_time": start_time,
            "end_time": end_time
        }

        response = self.app.post("/api/reservation", headers=self.headers, json=data)
        return response

    def cancel_reservation(self, user_id, reservation_id):
        data = {
            "user_id": user_id,
            "reservation_id": reservation_id
        }
        response = self.app.put("/api/reservation", headers=self.headers, json=data)
        return response


class ReservationTest(BasicTest):
    def setUp(self):
        self.checker_patcher = patch.object(ResourceChecker, 'check_building_available')
        self.mock_check = self.checker_patcher.start()
        self.mock_check.return_value = ({"message": "Building is available."}, 200)
        self.time_patcher = patch.object(TimeService, 'get_current_time')
        self.mock_time = self.time_patcher.start()
        self.mock_time.return_value = datetime(2024, 4, 15, 11, 00, 0)
        self.seat_util = SeatUtil()
        self.room_util = RoomUtil()
        self.student_util = StudentUtil()
        self.reservation_util = ReservationUtil()

    def tearDown(self):
        self.checker_patcher.stop()
        self.time_patcher.stop()

    def test_create_reservation_successfully(self):
        self.room_util.create_room()
        self.seat_util.create_seat()
        self.student_util.create_student()
        response = self.reservation_util.create_reservation()
        self.assertEqual(response.status_code, 201)

    def test_create_reservation_without_student(self):
        self.room_util.create_room()
        self.seat_util.create_seat()
        response = self.reservation_util.create_reservation()
        self.assertEqual(response.status_code, 404)

    def test_create_reservation_without_room(self):
        self.room_util.create_room()
        self.seat_util.create_seat()
        self.student_util.create_student()
        response = self.reservation_util.create_reservation(room_id=2)
        self.assertEqual(response.status_code, 404)

    def test_create_reservation_with_deprecated_room(self):
        self.room_util.create_room()
        self.seat_util.create_seat()
        self.room_util.delete_room(1)
        self.student_util.create_student()
        response = self.reservation_util.create_reservation()
        self.assertEqual(response.status_code, 400)

    def test_create_reservation_without_seat(self):
        self.room_util.create_room()
        self.student_util.create_student()
        response = self.reservation_util.create_reservation()
        self.assertEqual(response.status_code, 404)

    def test_create_reservation_with_deprecated_seat(self):
        self.room_util.create_room()
        self.seat_util.create_seat()
        self.seat_util.delete_seat(1)
        self.student_util.create_student()
        response = self.reservation_util.create_reservation()
        self.assertEqual(response.status_code, 400)

    def test_create_reservation_with_dismatch_seat(self):
        self.room_util.create_room()
        self.room_util.create_room()
        self.seat_util.create_seat(room_id=2)
        self.student_util.create_student()
        response = self.reservation_util.create_reservation()
        self.assertEqual(response.status_code, 400)

    def test_create_reservation_with_dismatch_school(self):
        self.room_util.create_room(school="Liberty")
        self.seat_util.create_seat()
        self.student_util.create_student()
        response = self.reservation_util.create_reservation()
        self.assertEqual(response.status_code, 400)

    def test_create_reservation_with_bad_time(self):
        self.room_util.create_room()
        self.seat_util.create_seat()
        self.student_util.create_student()
        response = self.reservation_util.create_reservation(start_time="2024:05:20:15:00:00")
        self.assertEqual(response.status_code, 400)
        
        response = self.reservation_util.create_reservation(
            start_time="2024-05-20 15:00:00", end_time="2024-05-20 13:00:00")
        self.assertEqual(response.status_code, 400)
        
        response = self.reservation_util.create_reservation(
            start_time="2024-05-20 15:00:00", end_time="2024-05-21 13:00:00")
        self.assertEqual(response.status_code, 400)
        
        response = self.reservation_util.create_reservation(
            start_time="2024-04-15 09:00:00", end_time="2024-04-15 12:00:00")
        self.assertEqual(response.status_code, 400)
        
        response = self.reservation_util.create_reservation(
            start_time="2024-05-20 15:00:00", end_time="2024-05-20 15:30:00")
        self.assertEqual(response.status_code, 400)

        response = self.reservation_util.create_reservation(
            start_time="2024-05-20 09:00:00", end_time="2024-05-20 16:00:00")
        self.assertEqual(response.status_code, 400)

        response = self.reservation_util.create_reservation(
            start_time="2024-05-20 01:00:00", end_time="2024-05-20 03:00:00")
        self.assertEqual(response.status_code, 400)

        response = self.reservation_util.create_reservation(
            start_time="2024-05-20 21:00:00", end_time="2024-05-20 22:00:00")
        self.assertEqual(response.status_code, 400)

    def test_create_reservation_with_conflict(self):
        self.room_util.create_room()
        self.seat_util.create_seat()
        self.student_util.create_student()
        self.reservation_util.create_reservation()
        response = self.reservation_util.create_reservation()
        self.assertEqual(response.status_code, 400)

    def test_cancel_reservation_successfully(self):
        self.room_util.create_room()
        self.seat_util.create_seat()
        self.student_util.create_student()
        self.reservation_util.create_reservation()
        response = self.reservation_util.cancel_reservation(1, 1)
        self.assertEqual(response.status_code, 200)

    def test_cancel_reservation_with_wrong_user(self):
        self.room_util.create_room()
        self.seat_util.create_seat()
        self.student_util.create_student()
        self.student_util.create_student(student_id="123")
        self.reservation_util.create_reservation()
        response = self.reservation_util.cancel_reservation(2, 1)
        self.assertEqual(response.status_code, 400)