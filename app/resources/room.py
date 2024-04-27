from datetime import time
from flask_restful import Resource, reqparse
from models import Room, Building
from utils.logz import create_logger
from utils.time import check_time_slot

class RoomResource(Resource):
    def __init__(self):
        self.logger = create_logger("room")

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
        if building.deprecated:
            return {"message": "Buidling id has been deprecated."}, 400

        check_time_slot(args["open_time"], args["close_time"])

        room = Room(**args)
        room.save_to_db()

        return {"message": "Room created successfully."}, 201