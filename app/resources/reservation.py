from datetime import datetime, time
from flask import request
from flask_restful import Resource, reqparse
from models import AdminConfig, Reservation, Room, Student
from utils.logz import create_logger
from utils.time import TimeService
from utils.resource_checker import ResourceChecker

class ReservationResource(Resource):
    def __init__(self):
        self.logger = create_logger("reservation")

    def get(self):
        room_id = request.args.get("room_id", type=int)
        seat_id = request.args.get("seat_id", type=int)
        if seat_id is None:
            reservations = Reservation.query.filter_by(room_id=room_id).all()
        else:
            reservations = Reservation.query.filter_by(room_id=room_id, seat_id=seat_id).all()

        if not reservations:
            return {"message": "No reservations found for the specified room and seat combination."}, 404

        reservation_list = [reservation.to_dict() for reservation in reservations]

        return {"reservations": reservation_list}, 200


    # create reservation
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, required=True)
        parser.add_argument("room_id", type=int, required=True)
        parser.add_argument("seat_id", type=int, required=True)
        parser.add_argument("start_time", type=str, required=True)
        parser.add_argument("end_time", type=str, required=True)

        args = dict(parser.parse_args())

        student = Student.find_by_id(args["user_id"])
        if student is None:
            return {"message": "Student not found."}, 404

        result, status_code = ResourceChecker.check_room_available(args["room_id"])
        if status_code != 200:
            return result, status_code

        result, status_code = ResourceChecker.check_seat_available(args["seat_id"])
        if status_code != 200:
            return result, status_code

        result, status_code = ResourceChecker.check_school_match(args["user_id"], args["room_id"])
        if status_code != 200:
            return result, status_code

        try:
            start_time = datetime.strptime(args["start_time"], '%Y-%m-%d %H:%M:%S')
            end_time = datetime.strptime(args["end_time"], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return {"message": "Invalid time format. Please use '%Y-%m-%d %H:%M:%S'"}, 400
        if start_time > end_time:
            return {"message": "The start time is later than the end time."}, 400
        if start_time.date() != end_time.date():
            return {"message": "Reservation start and end times must be on the same day."}, 400
        if start_time < TimeService.get_current_time():
            return {"message": "Reservation time is earlier than current time."}, 400
        time_delta = end_time - start_time
        time_seconds = time_delta.total_seconds()
        if time_seconds % 3600 != 0:
            return {"message": "Reservation time must be an integral multiple of an hour."}, 400
        max_reservation_duration_config = AdminConfig.find_by_key("max_reservation_duration")
        if max_reservation_duration_config is None:
            max_reservation_duration = 4.0
        else:
            max_reservation_duration = max_reservation_duration_config.config_value
        if time_seconds / 3600 > float(max_reservation_duration):
            return {"message": "Exceeding the maximum reservation duration."}, 400

        room = Room.find_by_id(args["room_id"])
        if start_time.time() < room.open_time:
            return {"message": "Reservation start time is earlier than room open time."}, 400
        if end_time.time() > room.close_time:
            return {"message": "Reservation end time is later than room close time."}, 400

        seat_reservations = Reservation.find_by_seat_id(args["seat_id"])
        for r in seat_reservations:
            if r.status == 2 or r.status == 3:
                continue
            if TimeService.check_time_overlap(r.start_time, r.end_time, start_time, end_time):
                return {"message": "Reservation time conflicts with existing reservation."}, 400
        
        args["create_time"] = TimeService.get_current_time()
        args["status"] = 0

        reservation = Reservation(**args)
        reservation.save_to_db()

        return {"message": "Reservation created successfully."}, 201