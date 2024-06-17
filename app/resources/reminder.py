import requests

from db import db
from datetime import datetime, time
from flask import request
from flask_restful import Resource, reqparse
from models import Building, Reservation, Room, Seat, Student
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
        delay_once = TimeService.get_seconds_before(start_time, -15)
        if (delay_once > 0):
            self.once_reminder.create_reminder(delay_once, reservation_id)
        delay_twice = TimeService.get_seconds_before(start_time, 10)
        self.twice_reminder.create_reminder(delay_twice, reservation_id)
        delay_timeout = TimeService.get_seconds_before(start_time, 15)
        self.timeout_reminder.create_reminder(delay_timeout, reservation_id)

class Reminder:
    def create_reminder(self, delay, reservation_id):
        timer = Timer(delay, self.send_reminder, args=(reservation_id,))
        timer.start()

    def send_request(self, message):
        # TODO: get access token
        access_token = "MY_ACCESS_TOKEN"
        url = "https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token=" + access_token
        requests.post(url, json=message)


class OnceReminder(Reminder):
    def send_reminder(self, reservation_id):
        reservation = Reservation.find_by_id(reservation_id)
        if reservation.status != 0:
            return

        student = Student.find_by_id(reservation.user_id)
        room = Room.find_by_id(reservation.room_id)
        building = Building.find_by_id(room.building_id)
        start_time = reservation.start_time.strftime('%Y-%m-%d %H:%M:%S')
        end_time = reservation.end_time.strftime('%Y-%m-%d %H:%M:%S')

        message = {
            # TODO: get user token
            "touser": "??? todo",
            "template_id": "5Cdabe6_ge7um2uK88xJ8OwfprBqwKjQXCkclh-sbtQ",
            "miniprogram_state": "trial",
            "lang": "zh_CN",
            "data": {
                "name1": {
                    "value": student.name
                },
                "thing2": {
                    "value": building.name + " " + room.name + " " + reservation.seat_id
                },
                "time22": {
                    "value": start_time
                },
                "time23": {
                    "value": end_time
                }
            }
        }
        self.send_request(message)


class TwiceReminder(Reminder):
    def send_reminder(self, reservation_id):
        reservation = Reservation.find_by_id(reservation_id)
        if reservation.status != 0:
            return

        student = Student.find_by_id(reservation.user_id)
        room = Room.find_by_id(reservation.room_id)
        building = Building.find_by_id(room.building_id)
        start_time = reservation.start_time.strftime('%Y-%m-%d %H:%M:%S')
        end_time = reservation.end_time.strftime('%Y-%m-%d %H:%M:%S')

        message = {
            # TODO: get user token
            "touser": "??? todo",
            "template_id": "OcD8novN3sx8DP8-Sd2wZEpSmC7rIo0Po-3z7tI7SUo",
            "miniprogram_state": "trial",
            "lang": "zh_CN",
            "data": {
                "thing9": {
                    "value": student.name
                },
                "thing15": {
                    "value": building.name + " " + room.name + " " + reservation.seat_id
                },
                "character_string10": {
                    "value": start_time + "-" + end_time
                }
            }
        }
        self.send_request(message)


class TimeoutReminder(Reminder):
    def send_reminder(self, reservation_id):
        reservation = Reservation.find_by_id(reservation_id)
        if reservation.status != 0:
            return

        student = Student.find_by_id(reservation.user_id)
        room = Room.find_by_id(reservation.room_id)
        building = Building.find_by_id(room.building_id)
        start_time = reservation.start_time.strftime('%Y-%m-%d %H:%M:%S')
        end_time = reservation.end_time.strftime('%Y-%m-%d %H:%M:%S')

        message = {
            # TODO: get user token
            "touser": "??? todo",
            "template_id": "tqzj_BWEEZyBtq8RgFKrVE0rvknsDNzvUPDoKOG4U4k",
            "miniprogram_state": "trial",
            "lang": "zh_CN",
            "data": {
                "thing1": {
                    "value": student.name
                },
                "thing3": {
                    "value": building.name + " " + room.name + " " + reservation.seat_id
                },
                "thing4": {
                    "value": start_time + "-" + end_time
                }
            }
        }
        self.send_request(message)

        reservation.status = 2
        reservation.save_to_db()

        student.breach_count += 1
        student.save_to_db()