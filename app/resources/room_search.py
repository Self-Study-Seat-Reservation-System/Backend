from datetime import datetime
from flask import request
from flask_restful import Resource, reqparse
from models import Room
from utils.logz import create_logger

class RoomSearchResource(Resource):
    def __init__(self):
        self.logger = create_logger("room_search")
        
    def get(self):
        campus = request.args.get("campus", type=str)
        building_id = request.args.get("building", type=str)
        school = request.args.get("school", type=str)
        available = request.args.get("available", type=bool)

        rooms = Room.find_all()

        if campus:
            rooms = [room for room in rooms if room.campus == campus]
        
        if building_id:
            rooms = [room for room in rooms if room.building_id == building_id]
        
        if school:
            rooms = [room for room in rooms if room.school == school]

        if available is not None:
            current_time = datetime.now().time()
            rooms = [room for room in rooms if not room.deprecated and room.open_time <= current_time <= room.close_time]
            
        if not rooms:
            return {"message": "No rooms found."}, 404
        
        room_data = [room.to_dict() for room in rooms]

        return {"rooms": room_data}, 200
