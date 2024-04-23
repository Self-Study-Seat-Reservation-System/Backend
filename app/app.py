from flask import Flask
from flask_restful import Api

from initializers import mysql

from resources.hello import Hello
from resources.seat import SeatResource

app = Flask(__name__)
app.config.from_object("config.Config")

db = mysql.init_db(app)
api = Api(app)

api.add_resource(Hello, "/", "/api/hello")
api.add_resource(SeatResource, "/api/seat")

if __name__ == "__main__":
    app.run(debug=True)