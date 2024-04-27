from flask import request
from flask_restful import Resource, reqparse
from models import AdminConfig
from utils.logz import create_logger

class ConfigResource(Resource):
    def __init__(self):
        self.logger = create_logger("config")

    def get(self):
        # 获取当前的最大预约时长
        max_reservation_duration_config = AdminConfig.query.filter_by(config_key='max_reservation_duration').first()
        if max_reservation_duration_config:
            max_reservation_duration = max_reservation_duration_config.config_value
        else:
            # 如果没有设置过，默认为4小时
            max_reservation_duration = 4

        return {"max_reservation_duration": max_reservation_duration}, 200

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("max_reservation_duration", type=int, required=True, help="Max reservation duration must be an integer.")
        args = parser.parse_args()

        max_reservation_duration = args["max_reservation_duration"]

        if max_reservation_duration <= 0:
            return {"message": "Max reservation duration must be a positive integer."}, 400

        # 更新或创建最大预约时长配置
        max_reservation_duration_config = AdminConfig.query.filter_by(config_key='max_reservation_duration').first()
        if max_reservation_duration_config:
            max_reservation_duration_config.config_value = max_reservation_duration
        else:
            max_reservation_duration_config = AdminConfig(config_key='max_reservation_duration', config_value=max_reservation_duration)
        max_reservation_duration_config.save_to_db()

        return {"message": "Max reservation duration updated successfully."}, 200
