from datetime import datetime
from flask import request
from flask_restful import Resource, reqparse
from models import Room

class RoomSearchResource(Resource):
    def get(self):
        campus = request.args.get("campus", type=str)
        building = request.args.get("building", type=str)
        department = request.args.get("department", type=str)
        available = request.args.get("available", type=bool)

        query = Room.query

        if campus:
            query = query.filter(Room.campus == campus)
        
        if building:
            query = query.filter(Room.building == building)
        
        if department:
            query = query.filter(Room.department == department)

        if available is not None:
            current_time = datetime.now().time()
            query = query.filter(Room.deprecated == False)
            query = query.filter(Room.open_time <= current_time, Room.close_time >= current_time)

        rooms = query.all()
        if not rooms:
            return {"message": "No rooms found."}, 404
        
        room_data = [room.to_dict() for room in rooms]

        return {"rooms": room_data}, 200
