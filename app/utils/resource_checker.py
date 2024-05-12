from models import Building, Room, Seat, Student

class ResourceChecker:
    @staticmethod
    def check_building_available(id):
        building = Building.find_by_id(id)
        if not building:
            return {"message": "Building not found."}, 404
        if building.deprecated is True:
            return {"message": "Buidling id has been deprecated."}, 400
        return {"message": "Building is available."}, 200

    @staticmethod
    def check_room_available(id):
        room = Room.find_by_id(id)
        if not room:
            return {"message": "Room not found."}, 404
        if room.deprecated is True:
            return {"message": "Room id has been deprecated."}, 400
        return {"message": "Room is available."}, 200

    @staticmethod
    def check_seat_available(id):
        seat = Seat.find_by_id(id)
        if not seat:
            return {"message": "Seat not found."}, 404
        if seat.deprecated is True:
            return {"message": "Seat id has been deprecated."}, 400
        return {"message": "Seat is available."}, 200
    
    @staticmethod
    def check_school_match(user_id, room_id):
        user = Student.find_by_id(user_id)
        room = Room.find_by_id(room_id)
        if room.school is not None and user.school != room.school:
            return {"message": "Student of this school can't book this room."}, 400
        return {"message": "Student of this school can book this room."}, 200