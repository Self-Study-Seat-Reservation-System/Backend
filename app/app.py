from flask import Flask
from flask_restful import Api

from initializers import mysql

from resources.admin import AdminResource
from resources.adminconfig import ConfigResource
from resources.building import BuildingResource
from resources.hello import Hello
from resources.reservation import ReservationResource
from resources.room import RoomResource
from resources.seat import SeatResource
from resources.student import StudentResource


app = Flask(__name__)
app.config.from_object("config.Config")

db = mysql.init_db(app)
api = Api(app)

# admin
api.add_resource(AdminResource, "/api/admin")

# adminconfig
api.add_resource(ConfigResource, "/api/adminconfig")

# building
api.add_resource(BuildingResource, "/api/building", endpoint="building")
api.add_resource(BuildingResource, "/api/building/<int:building_id>", endpoint="building_by_id")

# hello
api.add_resource(Hello, "/", "/api/hello")

# reservation
api.add_resource(ReservationResource, "/api/reservation")

# room
api.add_resource(RoomResource, "/api/room", endpoint="room")
api.add_resource(RoomResource, "/api/room/<int:room_id>", endpoint="room_by_id")

# seat
api.add_resource(SeatResource, "/api/seat", endpoint="seat")
api.add_resource(SeatResource, "/api/seat/<int:seat_id>", endpoint="seat_by_id")

# student
api.add_resource(StudentResource, "/api/student")


if __name__ == "__main__":
    app.run(debug=True)