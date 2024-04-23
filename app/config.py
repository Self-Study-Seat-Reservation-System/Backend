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

mysqlConfig = "mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4" \
    .format(MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DATABASE)

class Config:
    SQLALCHEMY_DATABASE_URI = mysqlConfig
