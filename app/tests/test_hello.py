import sys
import os
sys.path.append(os.path.dirname(__file__))

import base_test

class HelloTest(base_test.BasicTest):
    def setUp(self):
        self.hello_util = base_test.BasicUtil()
    
    def test_hello(self):
        response = self.hello_util.app.get("/")
        self.assertEqual(response.status_code, 200)