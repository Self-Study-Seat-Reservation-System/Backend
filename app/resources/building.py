from flask_restful import Resource, reqparse
from models import Building
from utils.logz import create_logger
from utils.time import check_time_slot

class BuildingResource(Resource):
    def __init__(self):
        self.logger = create_logger("building")
    
    
    def get(self, building_id=None):
        if building_id:
            building = Building.find_by_id(building_id)
            if building:
                return building.to_dict(), 200
            return {"message": "Building not found."}, 404
        return {"buildings": [building.to_dict() for building in Building.find_all()]}, 200


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