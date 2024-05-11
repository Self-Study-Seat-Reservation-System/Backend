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

        query = Seat.query

        if available is not None:
            query = query.filter(Seat.deprecated == False)
        
        if near_window:
            query = query.filter(Seat.near_window == True)
        
        if near_fixed_socket:
            query = query.filter(Seat.near_fixed_socket == True)
        
        if near_movable_socket:
            query = query.filter(Seat.near_movable_socket == True)

        seats = query.all()
        if not seats:
            return {"message": "No seats found."}, 404
        seat_data = [seat.to_dict() for seat in seats]

        return {"seats": seat_data}, 200
