import sys
import os
sys.path.append(os.path.dirname(__file__))

from base_test import BasicTest, BasicUtil

class AdminConfigUtil(BasicUtil):
    def get_max_reservation_duration(self):
        response = self.app.get("/api/adminconfig")
        return response

    def update_max_reservation_duration(self, max_reservation_duration):
        data = {
            "max_reservation_duration": max_reservation_duration
        }

        response = self.app.put("/api/adminconfig", headers=self.headers, json=data)
        return response


class AdminConfigTest(BasicTest):
    def setUp(self):
        self.admin_config_util = AdminConfigUtil()
    
    def test_get_max_reservation_duration(self):
        self.admin_config_util.update_max_reservation_duration(5)
        response = self.admin_config_util.get_max_reservation_duration()
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("max_reservation_duration", data)

    def test_update_max_reservation_duration(self):
        response = self.admin_config_util.update_max_reservation_duration(6)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Max reservation duration updated successfully.", response.json["message"])

    def test_update_max_reservation_duration_negative(self):
        response = self.admin_config_util.update_max_reservation_duration(-1)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Max reservation duration must be a positive integer.", response.json["message"])

    def test_update_max_reservation_duration_zero(self):
        response = self.admin_config_util.update_max_reservation_duration(0)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Max reservation duration must be a positive integer.", response.json["message"])