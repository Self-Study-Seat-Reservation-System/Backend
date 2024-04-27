from flask import Flask
from flask_restful import Api

from initializers import mysql

from resources.building import BuildingResource
from resources.hello import Hello
from resources.room import RoomResource
from resources.seat import SeatResource
from resources.reservation import ReservationResource
from resources.adminconfig import ConfigResource

app = Flask(__name__)
app.config.from_object("config.Config")

db = mysql.init_db(app)
api = Api(app)

api.add_resource(BuildingResource, "/api/building")
api.add_resource(Hello, "/", "/api/hello")
api.add_resource(RoomResource, "/api/room")
api.add_resource(SeatResource, "/api/seat")
api.add_resource(ReservationResource, "/api/reservation")
api.add_resource(ConfigResource, "/api/config")

if __name__ == "__main__":
    app.run(debug=True)