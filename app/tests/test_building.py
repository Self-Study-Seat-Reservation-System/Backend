import sys
import os
sys.path.append(os.path.dirname(__file__))

from base_test import BasicTest, BasicUtil

class BuildingUtil(BasicUtil):
    def create_building(self):
        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "name": "Building Name",
            "campus": "Campus Name",
            "open_time": "08:00:00",
            "close_time": "17:00:00"
        }

        response = self.app.post("/api/building", headers=headers, json=data)
        return response


class BuildingTest(BasicTest):
    def setUp(self):
        self.building_util = BuildingUtil()
    
    def test_building_create_successfully(self):
        response = self.building_util.create_building()
        self.assertEqual(response.status_code, 201)