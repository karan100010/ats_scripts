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
        self.API_ENDPOINT = config.AIRFLOW_API_HOST

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
        self.make_request("/health","GET")        

    def test_response_body_not_empty(self):
        
        self.assertTrue(self.response.json().get('dag_processor'))
        self.assertTrue(self.response.json().get('metadatabase'))
        self.assertTrue(self.response.json().get('scheduler'))
        self.assertTrue(self.response.json().get('triggerer'))

    def test_response_body_structure_correct(self):
        self.assertIsInstance(self.response.json().get('dag_processor'), object)
        self.assertIsInstance(self.response.json().get('metadatabase'), object)
        self.assertIsInstance(self.response.json().get('scheduler'), object)
        self.assertIsInstance(self.response.json().get('triggerer'), object)
   
    def test_response_values(self):
        self.assertEqual(self.response.json().get('metadatabase')['status'], 'healthy')
        self.assertEqual(self.response.json().get('scheduler')['status'], 'healthy')
        self.assertEqual(self.response.json().get('triggerer')['status'], 'healthy')
        

    

    


    
    
   