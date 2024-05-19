import sys
import os
sys.path.append(os.path.dirname(__file__))

from base_test import BasicTest, BasicUtil
from test_building import BuildingUtil

class RoomUtil(BasicUtil):
    def create_room(self, building_id=1, school="", name="A6025", open_time="08:00:00", close_time="17:00:00"):
        data = {
            "building_id": building_id,
            "name": name,
            "open_time": open_time,
            "close_time": close_time
        }

        if school:
            data["school"] = school

        response = self.app.post("/api/room", headers=self.headers, json=data)
        return response

    def delete_room(self, room_id):
        response = self.app.delete(f"/api/room/{room_id}")
        return response


class RoomTest(BasicTest):
    def setUp(self):
        self.room_util = RoomUtil()
        self.building_util = BuildingUtil()

    def test_create_room_without_school(self):
        self.building_util.create_building()
        response = self.room_util.create_room()
        self.assertEqual(response.status_code, 201)
    
    def test_create_room_with_school(self):
        self.building_util.create_building()
        response = self.room_util.create_room(school="computer")
        self.assertEqual(response.status_code, 201)

    def test_create_room_without_building(self):
        response = self.room_util.create_room(school="computer")
        self.assertEqual(response.status_code, 404)

    def test_delete_room_successfully(self):
        self.building_util.create_building()
        self.room_util.create_room()
        response = self.room_util.delete_room(1)
        self.assertEqual(response.status_code, 200)

    def test_delete_room_without_room(self):
        response = self.room_util.delete_room(1)
        self.assertEqual(response.status_code, 404)