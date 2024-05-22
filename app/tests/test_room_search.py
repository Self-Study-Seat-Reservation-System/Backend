import sys
import os
sys.path.append(os.path.dirname(__file__))

from base_test import BasicTest, BasicUtil
from test_building import BuildingUtil
from test_room import RoomUtil

class RoomSearchTest(BasicTest):
    def setUp(self):
        self.building_util = BuildingUtil()
        self.room_util = RoomUtil()
    
    def test_search_room_by_campus(self):
        self.building_util.create_building(campus="H")
        self.building_util.create_building(campus="B")
        self.room_util.create_room(school="Math", building_id=1)
        self.room_util.create_room(school="Computer", building_id=2)
        self.room_util.create_room(school="Math", building_id=2)
        response = self.room_util.app.get("/api/room/search?campus=H")
        self.assertEqual(response.status_code, 200)
        data = response.json
        expected_response = {
            "rooms": [
                {
                    "id": 1,
                    "building_id": 1,
                    "school": "Math",
                    "name": "A6025",
                    "open_time": "08:00:00",
                    "close_time": "17:00:00",
                    "deprecated": False
                }
            ]
        }
        self.assertEqual(data, expected_response)

    def test_search_room_by_building_id(self):
        self.building_util.create_building(campus="H")
        self.building_util.create_building(campus="J")
        self.room_util.create_room(building_id=1, school="Math")
        self.room_util.create_room(building_id=2, school="Computer")
        self.room_util.create_room(building_id=2, school="Physics")
        response = self.room_util.app.get("/api/room/search?building=1")
        self.assertEqual(response.status_code, 200)
        data = response.json
        expected_response = {
            "rooms": [
                {
                    "id": 1,
                    "building_id": 1,
                    "school": "Math",
                    "name": "A6025",
                    "open_time": "08:00:00",
                    "close_time": "17:00:00",
                    "deprecated": False
                }
            ]
        }
        self.assertEqual(data, expected_response)

    def test_search_room_by_school(self):
        self.building_util.create_building()
        self.room_util.create_room(school="Computer")
        self.room_util.create_room(school="Math")
        self.room_util.create_room(school="Computer")
        response = self.room_util.app.get("/api/room/search?school=Computer")
        self.assertEqual(response.status_code, 200)
        data = response.json
        expected_response = {
            "rooms": [
                {
                    "id": 1,
                    "building_id": 1,
                    "school": "Computer",
                    "name": "A6025",
                    "open_time": "08:00:00",
                    "close_time": "17:00:00",
                    "deprecated": False
                },
                {
                    "id": 3,
                    "building_id": 1,
                    "school": "Computer",
                    "name": "A6025",
                    "open_time": "08:00:00",
                    "close_time": "17:00:00",
                    "deprecated": False
                }
            ]
        }
        self.assertEqual(data, expected_response)

    def test_search_room_by_availability(self):
        self.building_util.create_building()
        self.room_util.create_room(school="Computer", open_time="08:00:00", close_time="23:00:00")
        self.room_util.create_room(school="Computer", open_time="09:00:00", close_time="23:00:00")
        self.room_util.create_room(school="Math", open_time="00:00:00", close_time="07:00:00")
        response = self.room_util.app.get("/api/room/search?available=true")
        self.assertEqual(response.status_code, 200)
        data = response.json
        expected_response = {
            "rooms": [
                {
                    "id": 1,
                    "building_id": 1,
                    "school": "Computer",
                    "name": "A6025",
                    "open_time": "08:00:00",
                    "close_time": "23:00:00",
                    "deprecated": False
                },
                {
                    "id": 2,
                    "building_id": 1,
                    "school": "Computer",
                    "name": "A6025",
                    "open_time": "09:00:00",
                    "close_time": "23:00:00",
                    "deprecated": False
                }
            ]
        }
        self.assertEqual(data, expected_response)
        
    def test_search_room_by_all_parameters(self):
        self.building_util.create_building(campus="H")
        self.building_util.create_building(campus="J")
        self.building_util.create_building(campus="H")
        self.room_util.create_room(school="Computer", building_id=1, open_time="08:00:00", close_time="23:00:00")
        self.room_util.create_room(school="Computer", building_id=2, open_time="08:00:00", close_time="23:00:00")
        self.room_util.create_room(school="Math", building_id=3, open_time="08:00:00", close_time="23:00:00")
        response = self.room_util.app.get("/api/room/search?campus=H&building=1&available=true")
        self.assertEqual(response.status_code, 200)
        data = response.json
        expected_response = {
            "rooms": [
                {
                    "id": 1,
                    "building_id": 1,
                    "school": "Computer",
                    "name": "A6025",
                    "open_time": "08:00:00",
                    "close_time": "23:00:00",
                    "deprecated": False
                }
            ]
        }
        self.assertEqual(data, expected_response)
        
    def test_search_room_no_result(self):
        response = self.room_util.app.get("/api/room/search")
        self.assertEqual(response.status_code, 404)
        data = response.json
        expected_response = {"message": "No rooms found."}
        self.assertEqual(data, expected_response)
        self.assertIn("message", data)