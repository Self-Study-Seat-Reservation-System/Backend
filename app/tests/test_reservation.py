import sys
import os
sys.path.append(os.path.dirname(__file__))

from base_test import BasicTest, BasicUtil
from datetime import datetime
from flask import url_for
from test_building import BuildingUtil
from test_room import RoomUtil
from test_seat import SeatUtil
from test_student import StudentUtil
from unittest.mock import patch
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

    def get_reservation(self, user_id=None, room_id=None, seat_id=None):
        url = f"/api/reservation?user_id={user_id}&room_id={room_id}&seat_id={seat_id}"    
        response = self.app.get(url)
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
        self.time_patcher = patch.object(TimeService, 'get_current_time')
        self.mock_time = self.time_patcher.start()
        self.mock_time.return_value = datetime(2024, 4, 15, 11, 00, 0)
        
        self.building_util = BuildingUtil()
        self.seat_util = SeatUtil()
        self.room_util = RoomUtil()
        self.student_util = StudentUtil()
        self.reservation_util = ReservationUtil()

        self.building_util.create_building()

    def tearDown(self):
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

    def test_cancel_reservation_without_reservation(self):
        self.room_util.create_room()
        self.seat_util.create_seat()
        self.student_util.create_student()
        response = self.reservation_util.cancel_reservation(1, 1)
        self.assertEqual(response.status_code, 404)

    def test_cancel_reservation_with_wrong_user(self):
        self.room_util.create_room()
        self.seat_util.create_seat()
        self.student_util.create_student()
        self.student_util.create_student(student_id="2")
        self.reservation_util.create_reservation()
        response = self.reservation_util.cancel_reservation(2, 1)
        self.assertEqual(response.status_code, 400)

    def test_cancel_reservation_cancelled(self):
        self.room_util.create_room()
        self.seat_util.create_seat()
        self.student_util.create_student()
        self.reservation_util.create_reservation()
        self.reservation_util.cancel_reservation(1, 1)
        response = self.reservation_util.cancel_reservation(1, 1)
        self.assertEqual(response.status_code, 400)

    def test_get_reservation(self):
        for i in range(4):
            self.room_util.create_room(name=f"room{i}")
        self.seat_util.create_seat(room_id=3)
        self.seat_util.create_seat(room_id=4)
        self.student_util.create_student(student_id="1")
        self.student_util.create_student(student_id="2")
        self.reservation_util.create_reservation(user_id=1, room_id=3, seat_id=1)
        self.reservation_util.create_reservation(user_id=1, room_id=4, seat_id=2)
        self.reservation_util.create_reservation(user_id=2, room_id=4, seat_id=2,
                start_time="2024-05-20 09:00:00", end_time="2024-05-20 10:00:00")

        response = self.reservation_util.get_reservation()
        expected_response = {'reservations': [
            {'id': 3, 'user_id': 2, 'room_id': 4, 'seat_id': 2, 'create_time': '2024-04-15T11:00:00', 'start_time': '2024-05-20T09:00:00', 'end_time': '2024-05-20T10:00:00', 'status': 0, 'room_name': 'room3', 'building_name': 'Name1'}, 
            {'id': 1, 'user_id': 1, 'room_id': 3, 'seat_id': 1, 'create_time': '2024-04-15T11:00:00', 'start_time': '2024-05-20T15:00:00', 'end_time': '2024-05-20T16:00:00', 'status': 0, 'room_name': 'room2', 'building_name': 'Name1'}, 
            {'id': 2, 'user_id': 1, 'room_id': 4, 'seat_id': 2, 'create_time': '2024-04-15T11:00:00', 'start_time': '2024-05-20T15:00:00', 'end_time': '2024-05-20T16:00:00', 'status': 0, 'room_name': 'room3', 'building_name': 'Name1'}]}
        self.assertEqual(response.get_json(), expected_response)

        response = self.reservation_util.get_reservation(user_id=2)
        expected_response = {'reservations': [
            {'id': 3, 'user_id': 2, 'room_id': 4, 'seat_id': 2, 'create_time': '2024-04-15T11:00:00', 'start_time': '2024-05-20T09:00:00', 'end_time': '2024-05-20T10:00:00', 'status': 0, 'room_name': 'room3', 'building_name': 'Name1'}]}  
        self.assertEqual(response.get_json(), expected_response)

        response = self.reservation_util.get_reservation(seat_id=1)
        expected_response = {'reservations': [
            {'id': 1, 'user_id': 1, 'room_id': 3, 'seat_id': 1, 'create_time': '2024-04-15T11:00:00', 'start_time': '2024-05-20T15:00:00', 'end_time': '2024-05-20T16:00:00', 'status': 0, 'room_name': 'room2', 'building_name': 'Name1'}]}
        self.assertEqual(response.get_json(), expected_response)

        response = self.reservation_util.get_reservation(room_id=3)
        expected_response = {'reservations': [
            {'id': 1, 'user_id': 1, 'room_id': 3, 'seat_id': 1, 'create_time': '2024-04-15T11:00:00', 'start_time': '2024-05-20T15:00:00', 'end_time': '2024-05-20T16:00:00', 'status': 0, 'room_name': 'room2', 'building_name': 'Name1'}]}
        self.assertEqual(response.get_json(), expected_response)

        response = self.reservation_util.get_reservation(user_id=1, room_id=3)
        expected_response = {'reservations': [
            {'id': 1, 'user_id': 1, 'room_id': 3, 'seat_id': 1, 'create_time': '2024-04-15T11:00:00', 'start_time': '2024-05-20T15:00:00', 'end_time': '2024-05-20T16:00:00', 'status': 0, 'room_name': 'room2', 'building_name': 'Name1'}]}
        self.assertEqual(response.get_json(), expected_response)

        response = self.reservation_util.get_reservation(user_id=3)
        self.assertEqual(response.status_code, 404)