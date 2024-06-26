import sys
import os
sys.path.append(os.path.dirname(__file__))

from base_test import BasicTest, BasicUtil
from test_building import BuildingUtil

class RoomUtil(BasicUtil):
    def create_room(self, building_id=1, school=None, name="A6025", open_time="08:00:00", close_time="17:00:00"):
        data = {
            "building_id": building_id,
            "name": name,
            "open_time": open_time,
            "close_time": close_time
        }

        if school is not None:
            data["school"] = school

        response = self.app.post("/api/room", headers=self.headers, json=data)
        return response

    def update_room(self, room_id, open_time=None, close_time=None, deprecated=None):
        data = {k: v for k, v in {
            "open_time": open_time,
            "close_time": close_time,
            "deprecated": deprecated
        }.items() if v is not None}
        
        response = self.app.put(f"/api/room/{room_id}", headers=self.headers, json=data)
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

    def test_update_room_successfully(self):
        self.building_util.create_building()
        self.room_util.create_room()
        response = self.room_util.update_room(1, "15:00:00", "18:00:00", 0)
        self.assertEqual(response.status_code, 200)

    def test_update_room_without_room(self):
        response = self.room_util.update_room(1, "15:00:00", "18:00:00", 0)
        self.assertEqual(response.status_code, 404)

    def test_update_room_with_bad_time(self):
        self.building_util.create_building()
        self.room_util.create_room(open_time="05:00:00", close_time="18:00:00")
        response = self.room_util.update_room(room_id=1, open_time="19:00:00")
        self.assertEqual(response.status_code, 400)
        response = self.room_util.update_room(room_id=1, close_time="xx:00:00")
        self.assertEqual(response.status_code, 400)
        response = self.room_util.update_room(room_id=1, open_time="17:00:00", close_time="15:00:00")
        self.assertEqual(response.status_code, 400)