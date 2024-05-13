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
    
    def test_create_multiple_students_successfully(self):
        response = self.student_util.create_student(student_id="12345678902", name="Jane Smith")
        self.assertEqual(response.status_code, 201)

        response = self.student_util.create_student(student_id="12345678903", name="Alice Johnson")
        self.assertEqual(response.status_code, 201)

    def test_create_student_with_existing_id(self):
        self.student_util.create_student()
        response = self.student_util.create_student()
        self.assertEqual(response.status_code, 400)
    
    def test_create_student_with_non_student_id(self):
        response = self.student_util.create_student(student_id="")
        self.assertEqual(response.status_code, 400)

    def test_create_student_with_non_name(self):
        response = self.student_util.create_student(name="")
        self.assertEqual(response.status_code, 400)
    
    def test_create_student_with_non_password(self):
        response = self.student_util.create_student(password="")
        self.assertEqual(response.status_code, 400)
        
    def test_delete_student(self):
        self.student_util.create_student()
        response = self.student_util.delete_student()
        self.assertEqual(response.status_code, 200)

    def test_delete_multiple_students(self):
        self.student_util.create_student(student_id="12345678902", name="Jane Smith")
        self.student_util.create_student(student_id="12345678903", name="Alice Johnson")
        response = self.student_util.delete_student(student_id="12345678902")
        self.assertEqual(response.status_code, 200)
        response = self.student_util.delete_student(student_id="12345678903")
        self.assertEqual(response.status_code, 200)
        
    def test_delete_non_existing_student(self):
        response = self.student_util.delete_student()
        self.assertEqual(response.status_code, 400)

    def test_get_student(self):
        self.student_util.create_student()
        response = self.student_util.get_student()
        self.assertEqual(response.status_code, 200)

    def test_get_non_existing_student(self):
        response = self.student_util.get_student()
        self.assertEqual(response.status_code, 404)

