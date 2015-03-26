import unittest
import json
from pyreally.responses import Response
from pyreally import R

class TestResponse(unittest.TestCase):
    def test_properties(self):
        input = """{
         "tx": 15,
         "r": "/users/1134",
         "body": {"username": "ahmed", "email": "ahmed@email.com"}
         }"""
        response = Response(json.loads(input))
        self.assertEqual(response.body, {"username": "ahmed", "email": "ahmed@email.com"})
        self.assertEqual(response.r, R("/users/1134"))
        self.assertEqual(response.tx, 15)