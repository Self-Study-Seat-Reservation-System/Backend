import os
import sys
import json
from dotenv import load_dotenv

load_dotenv() # Load .env file

##################
# MYSQL SETTINGS #
##################
MYSQL_USER = os.getenv("MYSQL_USER", default="root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", default="")
MYSQL_HOST = os.getenv("MYSQL_HOST", default="localhost")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", default="seat_reservation")
HOST_IP = os.getenv("HOST_IP", default="0.0.0.0")
HOST_PORT = os.getenv("HOST_PORT", default="5000")

mysqlConfig = "mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4" \
    .format(MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DATABASE)


##################
# WX SETTINGS    #
##################
APPID = os.getenv("APPID", default="")
SECRET = os.getenv("SECRET", default="")

class Config:
    SQLALCHEMY_DATABASE_URI = mysqlConfig
    HOST_IP = HOST_IP
    HOST_PORT = HOST_PORT
    APPID = APPID
    SECRET = SECRET
