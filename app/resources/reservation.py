from datetime import time
from flask import request
from flask_restful import Resource, reqparse
from models import Reservation
from utils.logz import create_logger

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
