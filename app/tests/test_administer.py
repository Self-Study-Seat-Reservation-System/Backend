import sys
import os
sys.path.append(os.path.dirname(__file__))

from base_test import BasicTest, BasicUtil
from test_student import StudentUtil

class AdministerUtil(BasicUtil):
    def get_students_with_breach(self, breach_count):
        headers = {
            "Content-Type": "application/json"
        }
        response = self.app.get(f"/api/administer?breach_count={breach_count}", headers=headers)
        return response

class AdministerResourceTest(BasicTest):
    def setUp(self):
        self.administer_util = AdministerUtil()
        self.student_util = StudentUtil()

    def test_get_students_with_breach(self):
        self.student_util.create_student(breach_count=3)
        response = self.administer_util.get_students_with_breach(2)
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("breach_records", data)

    def test_get_no_students_with_breach(self):
        response = self.administer_util.get_students_with_breach(5)
        self.assertEqual(response.status_code, 404)
        data = response.json
        self.assertIn("No students with breach records greater than 5 found.", data["message"])