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
        self.building_util.create_building()
        self.room_util.create_room(school="H")
        response = self.room_util.app.get("/api/room/search?campus=H")
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("rooms", data)

    def test_search_room_by_building_id(self):
        self.building_util.create_building()
        self.room_util.create_room()
        response = self.room_util.app.get("/api/room/search?building=1")
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("rooms", data)

    def test_search_room_by_school(self):
        self.building_util.create_building()
        self.room_util.create_room(school="Computer")
        response = self.room_util.app.get("/api/room/search?school=Computer")
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("rooms", data)

    def test_search_room_by_availability(self):
        self.building_util.create_building()
        self.room_util.create_room(school="H", open_time="08:00:00", close_time="23:00:00")
        self.room_util.create_room(school="H", open_time="09:00:00", close_time="23:00:00")
        response = self.room_util.app.get("/api/room/search?available=true")
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("rooms", data)
        
    def test_search_room_by_all_parameters(self):
        self.building_util.create_building()
        self.room_util.create_room(school="H", building_id=1, open_time="08:00:00", close_time="23:00:00")
        response = self.room_util.app.get("/api/room/search?campus=H&building=1&available=true")
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("rooms", data)
        
    def test_search_room_no_result(self):
        response = self.room_util.app.get("/api/room/search")
        self.assertEqual(response.status_code, 404)
        data = response.json
        self.assertIn("message", data)