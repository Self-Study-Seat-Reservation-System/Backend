from models import Building, Room, Seat

class ResourceChecker:
    @staticmethod
    def check_room_available(id):
        room = Room.find_by_id(id)
        if not room:
            return {"message": "Room not found."}, 404
        if room.deprecated is True:
            return {"message": "Room id has been deprecated."}, 400
        return {"message": "Room is available."}, 200

    @staticmethod
    def check_building_available(id):
        building = Building.find_by_id(id)
        if not building:
            return {"message": "Building not found."}, 404
        if building.deprecated is True:
            return {"message": "Buidling id has been deprecated."}, 400
        return {"message": "Building is available."}, 200