import sys
import os
sys.path.append(os.path.dirname(__file__))

from base_test import BasicTest, BasicUtil

class BuildingUtil(BasicUtil):
    def create_building(self, name="Name1", campus="H", open_time="08:00:00", close_time="17:00:00"):
        data = {
            "name": name,
            "campus": campus,
            "open_time": open_time,
            "close_time": close_time
        }

        response = self.app.post("/api/building", headers=self.headers, json=data)
        return response


class BuildingTest(BasicTest):
    def setUp(self):
        self.building_util = BuildingUtil()
    
    def test_create_building_successfully(self):
        response = self.building_util.create_building()
        self.assertEqual(response.status_code, 201)

    def test_create_multiple_building_successfully(self):
        response = self.building_util.create_building("Name1")
        self.assertEqual(response.status_code, 201)
        response = self.building_util.create_building("Name2")
        self.assertEqual(response.status_code, 201)

    def test_create_synonym_building(self):
        self.building_util.create_building("Name1")
        response = self.building_util.create_building("Name1")
        self.assertEqual(response.status_code, 400)

    def test_create_building_with_wrong_time_slot(self):
        response = self.building_util.create_building(open_time="19:23:45", close_time="08:00:00")
        self.assertEqual(response.status_code, 400)

    def test_create_building_with_bad_format_time(self):
        response = self.building_util.create_building(open_time="08:00:00", close_time="09:0000")
        self.assertEqual(response.status_code, 400)
        response = self.building_util.create_building(open_time="08:00:00", close_time="09:00!00")
        self.assertEqual(response.status_code, 400)
        response = self.building_util.create_building(open_time="08:00:00", close_time="9:00:00")
        self.assertEqual(response.status_code, 400)

    def test_get_single_building(self):
        self.building_util.create_building()
        response = self.building_util.app.get("/api/building/1")
        self.assertEqual(response.status_code, 200)

    def test_get_all_building(self):
        self.building_util.create_building("Name1")
        self.building_util.create_building("Name2")
        response = self.building_util.app.get("/api/building")
        self.assertEqual(response.status_code, 200)