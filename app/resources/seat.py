from db import db
from flask_restful import Resource, reqparse
from models import Room, Seat
from utils.logz import create_logger

class SeatResource(Resource):
    def __init__(self):
        self.logger = create_logger("seat")

    def get(self, seat_id=None):
        if seat_id:
            seat = Seat.find_by_id(seat_id)
            if seat:
                return seat.to_dict(), 200
            return {"message": "Seat not found."}, 404
        return {"seats": [seat.to_dict() for seat in Seat.find_all()]}, 200

    # create seat
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("room_id", type=int, required=True)
        parser.add_argument("near_fixed_socket", type=bool)
        parser.add_argument("near_movable_socket", type=bool)
        parser.add_argument("near_window", type=bool)
        args = parser.parse_args()

        room = Room.find_by_id(args["room_id"])
        if not room:
            return {"message": "Room not found."}, 404
        if room.deprecated is True:
            return {"message": "Room id has been deprecated."}, 400

        seat = Seat(**args)
        seat.save_to_db()

        return {"message": "Seat created successfully."}, 201


    # update seat
    def put(self, seat_id):
        parser = reqparse.RequestParser()
        parser.add_argument("near_fixed_socket", type=bool)
        parser.add_argument("near_movable_socket", type=bool)
        parser.add_argument("near_window", type=bool)
        parser.add_argument("deprecated", type=bool)
        args = parser.parse_args()

        seat = Seat.find_by_id(seat_id)
        if not seat:
            return {"message": "Seat not found."}, 404
        
        if args["near_fixed_socket"] is not None:
            seat.near_fixed_socket = args["near_fixed_socket"]
        if args["near_movable_socket"] is not None:
            seat.near_movable_socket = args["near_movable_socket"]
        if args["near_window"] is not None:
            seat.near_window = args["near_window"]
        if args["deprecated"] is not None:
            seat.deprecated = args["deprecated"]

        db.session.commit()
        return {"message": "Seat updated successfully."}, 200

        
    def delete(self, seat_id):
        seat = Seat.find_by_id(seat_id)
        if not seat:
            return {"message": "Seat not found."}, 404

        seat.deprecated = True

        db.session.commit()
        return {"message": "Seat deleted successfully."}, 200