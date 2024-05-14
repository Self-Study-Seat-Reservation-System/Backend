import sys
import os
sys.path.append(os.path.dirname(__file__))

from base_test import BasicTest, BasicUtil

class StudentUtil(BasicUtil):
    def create_student(self, student_id="23210240105", name="John Doe", password="password123", wechat_number="john_doe", school="Computer", breach_count=0):
        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "student_id": student_id,
            "name": name,
            "password": password,
            "wechat_number": wechat_number,
            "school": school,
            "breach_count": breach_count
        }

        response = self.app.post("/api/student", headers=headers, json=data)
        return response

    def get_student(self, student_id="23210240105"):
        response = self.app.get(f"/api/student/{student_id}")
        return response

    def delete_student(self, student_id="23210240105"):
        response = self.app.delete(f"/api/student/{student_id}")
        return response

class StudentTest(BasicTest):
    def setUp(self):
        self.student_util = StudentUtil()
    
    def test_create_student_successfully(self):
        response = self.student_util.create_student()
        self.assertEqual(response.status_code, 201)
