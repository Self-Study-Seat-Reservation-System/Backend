import sys
import os
sys.path.append(os.path.dirname(__file__))

from base_test import BasicTest, BasicUtil
from test_building import BuildingUtil

class RoomUtil(BasicUtil):
    def create_room(self, building_id=1, school="", name="A6025", open_time="08:00:00", close_time="17:00:00"):
        headers = {
            "Content-Type": "application/json"
        }

        if school == "":
            data = {
                "building_id": building_id,
                "name": name,
                "open_time": open_time,
                "close_time": close_time
            }
        else:
            data = {
                "building_id": building_id,
                "school": school,
                "name": name,
                "open_time": open_time,
                "close_time": close_time
            }

        response = self.app.post("/api/room", headers=headers, json=data)
        return response


class RoomTest(BasicTest):
    def setUp(self):
        self.room_util = RoomUtil()
        self.building_util = BuildingUtil()
    
    def test_create_room_without_school(self):
        self.building_util.create_building()
        response = self.room_util.create_room()
        self.assertEqual(response.status_code, 201)