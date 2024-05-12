from db import db
from flask_restful import Resource, reqparse
from models import Building, Room, Seat
from utils.logz import create_logger
from utils.time import TimeService
from utils.resource_checker import ResourceChecker

class RoomResource(Resource):
    def __init__(self):
        self.logger = create_logger("room")

    def get(self, room_id=None):
        if room_id:
            room = Room.find_by_id(room_id)
            if room:
                return room.to_dict(), 200
            return {"message": "Room not found."}, 404
        return {"room": [room.to_dict() for room in Room.find_all()]}, 200


    # create room
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("building_id", type=int, required=True)
        parser.add_argument("school", type=str)
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("open_time", type=str, required=True)
        parser.add_argument("close_time", type=str, required=True)

        args = parser.parse_args()

        result, status_code = ResourceChecker.check_building_available(args["building_id"])
        if status_code != 200:
            return result, status_code

        result, status_code = TimeService.check_time_slot(args["open_time"], args["close_time"])
        if status_code != 200:
            return result, status_code

        room = Room(**args)
        room.save_to_db()

        return {"message": "Room created successfully."}, 201


    # update room
    def put(self, room_id):
        parser = reqparse.RequestParser()
        parser.add_argument("open_time", type=str)
        parser.add_argument("close_time", type=str)
        parser.add_argument("deprecated", type=bool)
        args = parser.parse_args()

        room = Room.find_by_id(room_id)
        if not room:
            return {"message": "Room not found."}, 404
        
        if args["deprecated"] is not None:
            room.deprecated = args["deprecated"]
            seats = Seat.find_by_room_id(room_id)
            if seats:
                for seat in seats:
                    seat.deprecated = args["deprecated"]

        if args["open_time"] is not None:
            my_open_time = args["open_time"]
        else:
            my_open_time = room.open_time.strftime('%H:%M:%S')
        if args["close_time"] is not None:
            my_close_time = args["close_time"]
        else:
            my_close_time = room.close_time.strftime('%H:%M:%S')       
        result, status_code = TimeService.check_time_slot(my_open_time, my_close_time)
        if status_code != 200:
            return result, status_code
        room.open_time = my_open_time
        room.close_time = my_close_time
        
        db.session.commit()
        return {"message": "Room updated successfully."}, 200


    # set room to deprecated
    def delete(self, room_id):
        room = Room.find_by_id(room_id)
        if not room:
            return {"message": "Room not found."}, 404
        room.deprecated = True

        seats = Seat.find_by_room_id(room_id)
        if seats:
            for seat in seats:
                seat.deprecated = True
        
        db.session.commit()
        return {"message": "Room deleted successfully."}, 200