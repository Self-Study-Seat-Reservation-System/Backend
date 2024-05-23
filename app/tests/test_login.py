import sys
import os
sys.path.append(os.path.dirname(__file__))

from base_test import BasicTest, BasicUtil
from test_student import StudentUtil

class LoginUtil(BasicUtil):
    def login(self, student_id="23210240105", password="password123"):
        data = {
            "student_id": student_id,
            "password": password
        }
        response = self.app.post("/api/login", headers=self.headers, json=data)
        return response

class LoginTest(BasicTest):
    def setUp(self):
        self.login_util = LoginUtil()
        self.student_util = StudentUtil()

    def test_login_success(self):
        self.student_util.create_student()
        response = self.login_util.login()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['code'], 1)
        self.assertEqual(response.json['message'], "Login successful")

    def test_login_failure_wrong_password(self):
        self.student_util.create_student()
        response = self.login_util.login(password="wrong_password")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['code'], 0)
        self.assertEqual(response.json['message'], "Login failed. Invalid student ID or password.")

    def test_login_failure_nonexistent_user(self):
        response = self.login_util.login()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['code'], 0)
        self.assertEqual(response.json['message'], "Login failed. Invalid student ID or password.")

