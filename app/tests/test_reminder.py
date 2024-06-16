import sys
import os
sys.path.append(os.path.dirname(__file__))

from base_test import BasicTest, BasicUtil
from datetime import datetime
from flask import url_for
from resources.reminder import ReminderCreater
from test_building import BuildingUtil
from test_reservation import ReservationUtil
from test_room import RoomUtil
from test_seat import SeatUtil
from test_student import StudentUtil
from time import sleep
from unittest.mock import patch
from utils.time import TimeService

class ReminderTest(BasicTest):
    def setUp(self):
        self.time_patcher = patch.object(TimeService, 'get_current_time')
        self.mock_time = self.time_patcher.start()
        self.mock_time.return_value = datetime(2024, 4, 15, 11, 00, 0)
        self.reminder_patcher = patch.object(ReminderCreater, 'batch_create_reminder')
        self.mock_reminder = self.reminder_patcher.start()
        
        self.building_util = BuildingUtil()
        self.seat_util = SeatUtil()
        self.room_util = RoomUtil()
        self.student_util = StudentUtil()
        self.reservation_util = ReservationUtil()

        self.building_util.create_building()

    def tearDown(self):
        self.time_patcher.stop()
        self.reminder_patcher.stop()

    def test_reminder_once(self):
        self.room_util.create_room()
        self.seat_util.create_seat()
        self.student_util.create_student()
        self.reservation_util.create_reservation()
        self.mock_reminder.assert_called_once()

        