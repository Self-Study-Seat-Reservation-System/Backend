from datetime import datetime, time
from flask_restful import Resource, reqparse
from models import Building
from utils.logz import create_logger

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

        try:
            open_time = time.fromisoformat(args["open_time"])
            close_time = time.fromisoformat(args["close_time"])
        except ValueError:
            return {"message": "Invalid time format. Please use 'HH:MM:SS'."}, 400
    
        if open_time > close_time:
            return {"message": "The open time is later than the close time."}, 400

        building = Building(name=args["name"], campus=args["campus"], 
            open_time=open_time, close_time=close_time)
        building.save_to_db()

        return {"message": "Building created successfully."}, 201