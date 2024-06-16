from db import db
from datetime import datetime, time
from flask import request
from flask_restful import Resource, reqparse
from models import Reservation, Seat, Student
from threading import Timer
from utils.logz import create_logger
from utils.time import TimeService
from utils.resource_checker import ResourceChecker

class ReminderCreater:
    def __init__(self):
        self.once_reminder = OnceReminder()
        self.twice_reminder = TwiceReminder()
        self.timeout_reminder = TimeoutReminder()
    
    def batch_create_reminder(self, start_time, reservation_id):
        delay_once = TimeService.get_seconds_from(start_time, -15)
        if (delay_once > 0):
            self.once_reminder.create_reminder(delay_once, reservation_id)
        delay_twice = TimeService.get_seconds_from(start_time, 10)
        self.twice_reminder.create_reminder(delay_twice, reservation_id)
        delay_timeout = TimeService.get_seconds_from(start_time, 15)
        self.timeout_reminder.create_reminder(delay_timeout, reservation_id)

class Reminder:
    def create_reminder(self, delay, reservation_id):
        timer = Timer(delay, self.send_reminder, args=(reservation_id,))
        timer.start()

class OnceReminder(Reminder):
    def send_reminder(self, delay, reservation_id):
        pass

class TwiceReminder(Reminder):
    def send_reminder(reservation_id):
        pass

class TimeoutReminder(Reminder):
    def send_reminder(reservation_id):
        pass


