from db import db
from flask_restful import Resource, reqparse
import logging
from models import Student
from utils.logz import create_logger
from utils.wx import WX

class Login(Resource):
    def __init__(self):
        self.logger = self.create_logger("login")

    def create_logger(self, name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("student_id", type=str, required=True, help="Student ID is required")
        parser.add_argument("password", type=str, required=True, help="Password is required")
        parser.add_argument("code", type=str, required=True, help="Code is required")
        args = parser.parse_args()

        student_id = args["student_id"]
        password = args["password"]
        code = args["code"]

        openid_ret = WX.get_openid(code)
        if type(openid_ret) == str:
            return {"message": "Failed to get openid."}, 400
        else:
            openid = openid_ret["openid"]

        if self.verify_user(student_id, password, openid):
            self.logger.info(f"Student {student_id} logged in successfully.")
            return {"message": "Login successful", "code": 1, "student_id": student_id}, 200
        else:
            self.logger.warning(f"Failed login attempt for student {student_id}.")
            return {"message": "Login failed. Invalid student ID or password.", "code": 0}, 401

    def verify_user(self, student_id, password, openid):
        student = Student.find_by_student_id(student_id)
        if student and student.password == password:
            if student.openid != openid:
                student.openid = openid
                db.session.commit()
            return True
        return False



