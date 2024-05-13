from flask_restful import Resource, reqparse, request
from models import Student
from utils.logz import create_logger

class StudentResource(Resource):
    def __init__(self):
        self.logger = create_logger("student")

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("student_id", type=str, required=True)
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("password", type=str, required=True)
        parser.add_argument("wechat_number", type=str)
        parser.add_argument("school", type=str)
        parser.add_argument("breach_count", type=int)
        args = parser.parse_args()
        
        if not args["student_id"] or not args["name"] or not args["password"]:
            return {"message": "Student ID, name, and password are required."}, 400
        existing_student = Student.find_by_student_id(args["student_id"])
        if existing_student:
            return {"message": "Student with this student ID already exists."}, 400
        student = Student(**args)
        student.save_to_db()

        return {"message": "Student registered successfully."}, 201

    def delete(self, student_id):
        if not student_id:
            return {"message": "Student ID is required in the request."}, 400

        student = Student.find_by_student_id(student_id)
        if not student:
            return {"message": "Student with this student ID doesn't exist."}, 400

        student.delete_from_db()
        return {"message": "Student deleted successfully."}, 200
    
    def get(self, student_id):
        if not student_id:
            return {"message": "Student ID is required in the request."}, 400

        student = Student.find_by_student_id(student_id)
        if not student:
            return {"message": "Student with this student ID doesn't exist."}, 404
        
        return {"student": student.to_dict()}, 200
