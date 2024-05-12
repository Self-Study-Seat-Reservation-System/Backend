import unittest
from unittest.mock import MagicMock
from resources.seat_search import SeatSearchResource
from models import Seat
import sys
import os
sys.path.append(os.path.dirname(__file__))

class TestSeatSearchResource(unittest.TestCase):
    def setUp(self):
        self.resource = SeatSearchResource()

    def test_get_all_seats(self):
        # 模拟一个请求对象
        request = MagicMock()
        request.args = {"available": None, "near_window": None, "near_fixed_socket": None, "near_movable_socket": None}

        # 模拟 Seat.query.all() 方法的返回结果
        Seat.query.all = MagicMock(return_value=["seat1", "seat2", "seat3"])

        # 使用模拟的请求对象调用 get 方法
        response = self.resource.get()

        # 验证查询参数是否正确传递给了 Seat.query.filter 方法
        self.assertEqual(response[1], 200)

        # 验证查询结果是否正确返回
        self.assertEqual(response[0]["seats"], ["seat1", "seat2", "seat3"])

    def test_get_seats_near_window(self):
        # 模拟一个请求对象
        request = MagicMock()
        request.args = {"available": None, "near_window": True, "near_fixed_socket": None, "near_movable_socket": None}

        # 模拟 Seat.query.filter 方法的返回结果
        Seat.query.filter = MagicMock(return_value=["seat1", "seat2"])

        # 使用模拟的请求对象调用 get 方法
        response = self.resource.get()

        # 验证查询参数是否正确传递给了 Seat.query.filter 方法
        Seat.query.filter.assert_called_once_with(Seat.near_window == True)

        # 验证查询结果是否正确返回
        self.assertEqual(response[1], 200)
        self.assertEqual(response[0]["seats"], ["seat1", "seat2"])

if __name__ == "__main__":
    unittest.main()
