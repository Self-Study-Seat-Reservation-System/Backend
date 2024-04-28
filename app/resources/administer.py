from flask_restful import Resource, reqparse, request
from models import Student
from utils.logz import create_logger

class AdministerResource(Resource):
    def __init__(self):
        self.logger = create_logger("administer")

    def get(self):
        breach_count = request.args.get('breach_count')
        students_with_breach = Student.query.filter(Student.breach_count > breach_count).all()
        if not students_with_breach:
            return {"message": f"No students with breach records greater than {breach_count} found."}, 404

        breach_records = [{"student_id": student.student_id, "name": student.name, "breach_count": student.breach_count} for student in students_with_breach]
        return {"breach_records": breach_records}, 200
