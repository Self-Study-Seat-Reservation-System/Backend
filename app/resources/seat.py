from flask_restful import Resource, reqparse

from models import Seat

from utils.logz import create_logger

class SeatResource(Resource):
    def __init__(self):
        self.logger = create_logger("seat")

    def get(self, seat_id=None):
        if seat_id:
            seat = Seat.find_by_id(seat_id)
            if seat:
                return seat.to_dict()
            return {"message": "Seat not found."}, 404
        return {"seats": [seat.to_dict() for seat in Seat.find_all()]}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("room_id", type=int, required=True)
        parser.add_argument("near_fixed_socket", type=bool)
        parser.add_argument("near_movable_socket", type=bool)
        parser.add_argument("near_window", type=bool)
        args = parser.parse_args()

        seat = Seat(**args)
        seat.save_to_db()

        return {"message": "Seat created successfully."}, 201