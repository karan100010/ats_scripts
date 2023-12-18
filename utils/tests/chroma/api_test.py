import requests
import unittest
import sys
from pathlib import Path
# Add the parent directory (project root) to the sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from config import Config


class APITestCase(unittest.TestCase):

    def __init__(self, methodName='runTest', *args, **kwargs):
        super().__init__(methodName, *args, **kwargs)
        config = Config()
        self.API_ENDPOINT = config.CHROMA_API_HOST

    def test_status_code_is_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_response_is_json(self):
        self.assertEqual(self.response.headers['Content-Type'], 'application/json')

    def test_response_time_less_than_200ms(self):
        self.assertLess(self.response.elapsed.total_seconds() * 1000, 200)

    def make_request(self, endpoint,request_type, json_body=None, headers=None):
        self.API_ENDPOINT = self.API_ENDPOINT + endpoint
        
        if request_type == "GET":
            response = requests.get(self.API_ENDPOINT)
        elif request_type == "POST":
            response = requests.post(self.API_ENDPOINT, json=json_body, headers=headers)
        self.response = response
            


class APIStatusTest(APITestCase):

    def __init__(self, methodName='runTest', *args, **kwargs):
        super().__init__(methodName, *args, **kwargs)
        self.make_request("/api/v1/heartbeat","GET")        

    def test_response_body_not_empty(self):
        self.assertTrue(self.response.json().get('nanosecond heartbeat'))
        

    def test_response_contains_status_value(self):
        self.assertIsInstance(self.response.json().get('nanosecond heartbeat'), int)

    




    
    
   