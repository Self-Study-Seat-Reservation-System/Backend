from datetime import time
from flask import request
from flask_restful import Resource, reqparse
from models import Reservation
from utils.logz import create_logger
from utils.time import TimeService

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
        parser.add_argument("sead_id", type=int, required=True)
        parser.add_argument("start_time", type=str, required=True)
        parser.add_argument("end_time", type=str, required=True)

        args = dict(parser.parse_args())

        result, status_code = ResourceChecker.check_building_available(args["building_id"])
        if status_code != 200:
            return result, status_code
        
        result, status_code = ResourceChecker.check_room_available(args["room"])
        if status_code != 200:
            return result, status_code

        result, status_code = TimeService.check_time_slot(args["open_time"], args["close_time"])
        if status_code != 200:
            return result, status_code
        
        args["create_time"] = TimeService.get_current_time

        reservation = Reservation(**args)
        reservation.save_to_db()

        return {"message": "Room created successfully."}, 201