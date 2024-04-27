from datetime import datetime, time
from flask_restful import Resource, reqparse
from models import Building
from utils.logz import create_logger
from utils.time import check_time_slot

class BuildingResource(Resource):
    def __init__(self):
        self.logger = create_logger("building")

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("campus", type=str, required=True)
        parser.add_argument("open_time", type=str, required=True)
        parser.add_argument("close_time", type=str, required=True)

        args = parser.parse_args()

        old_building = Building.find_by_name(args["name"])
        if old_building:
            return {"message": "The Building name already exists."}, 400

        check_time_slot(args["open_time"], args["close_time"])

        building = Building(**args)
        building.save_to_db()

        return {"message": "Building created successfully."}, 201