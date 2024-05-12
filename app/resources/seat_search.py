from datetime import datetime
from flask import request
from flask_restful import Resource, reqparse
from models import Seat, Room
from utils.logz import create_logger

class SeatSearchResource(Resource):
    def __init__(self):
        self.logger = create_logger("seat_search")
        
    def get(self):
        available = request.args.get("available", type=bool)
        near_window = request.args.get("near_window", type=bool)
        near_fixed_socket = request.args.get("near_fixed_socket", type=bool)
        near_movable_socket = request.args.get("near_movable_socket", type=bool)

        seats = Seat.find_all()

        if available is not None:
            seats = [seat for seat in seats if not seat.deprecated]
        
        if near_window:
            seats = [seat for seat in seats if seat.near_window]
        
        if near_fixed_socket:
            seats = [seat for seat in seats if seat.near_fixed_socket]
        
        if near_movable_socket:
            seats = [seat for seat in seats if seat.near_movable_socket]
        
        if not seats:
            return {"message": "No seats found."}, 404
        seat_data = [seat.to_dict() for seat in seats]

        return {"seats": seat_data}, 200
