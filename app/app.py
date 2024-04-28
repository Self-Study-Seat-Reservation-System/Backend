from flask import Flask
from flask_restful import Api

from initializers import mysql

from resources.building import BuildingResource
from resources.hello import Hello
from resources.room import RoomResource
from resources.seat import SeatResource
from resources.reservation import ReservationResource
from resources.admin_config import AdminConfigResource
from resources.student import StudentResource
from resources.administer import AdministerResource


app = Flask(__name__)
app.config.from_object("config.Config")

db = mysql.init_db(app)
api = Api(app)

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

# adminconfig
api.add_resource(AdminConfigResource, "/api/adminconfig")
# administer
api.add_resource(AdministerResource, "/api/administer")

if __name__ == "__main__":
    app.run(debug=True)