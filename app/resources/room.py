from db import db
from flask_restful import Resource, reqparse
from models import Building, Room, Seat
from utils.logz import create_logger
from utils.time import check_time_slot

class RoomResource(Resource):
    def __init__(self):
        self.logger = create_logger("room")

    # create room
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("building_id", type=int, required=True)
        parser.add_argument("school", type=str)
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("open_time", type=str, required=True)
        parser.add_argument("close_time", type=str, required=True)

        args = parser.parse_args()

        building = Building.find_by_id(args["building_id"])
        if not building:
            return {"message": "Building id doesn't exist."}, 400
        if building.deprecated == True:
            return {"message": "Buidling id has been deprecated."}, 400

        check_time_slot(args["open_time"], args["close_time"])

        room = Room(**args)
        room.save_to_db()

        return {"message": "Room created successfully."}, 201


    # set room to available
    def put(self, room_id):
        room = Room.find_by_id(room_id)
        if not room:
            return {"message": "Room id doesn't exist."}, 400
        room.deprecated = False

        seats = Seat.find_by_room_id(room_id)
        if seats:
            for seat in seats:
                seat.deprecated = False
        
        db.session.commit()
        return {"message": "Room updated successfully."}, 200


    # set room to deprecated
    def delete(self, room_id):
        room = Room.find_by_id(room_id)
        if not room:
            return {"message": "Room id doesn't exist."}, 400
        room.deprecated = True

        seats = Seat.find_by_room_id(room_id)
        if seats:
            for seat in seats:
                seat.deprecated = True
        
        db.session.commit()
        return {"message": "Room deleted successfully."}, 200