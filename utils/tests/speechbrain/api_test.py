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
        self.API_ENDPOINT = config.SPEECHBRAIN_API_HOST 

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
        self.make_request("/api_status","GET")        

    def test_response_body_not_empty(self):
        
        self.assertTrue(self.response.json().get('message'))
        self.assertTrue(self.response.json().get('status'))

    def test_response_contains_status_value(self):
        self.assertIsInstance(self.response.json().get('status'), str)

    def test_response_body_structure_correct(self):
        self.assertIsInstance(self.response.json().get('status'), str)



class PredictLanguage(APITestCase):
    def __init__(self, methodName='runTest', *args, **kwargs):
        super().__init__(methodName, *args, **kwargs)
        data = {
            "filepath": "https://omniglot.com/soundfiles/udhr/udhr_th.mp3"
        }
        headers = {"Content-Type": "application/json"}
        self.make_request("/predict_language", "POST", json_body=data, headers=headers)

    def test_entity_information_present(self):
        self.assertIsInstance(self.response.json(), object)

    def test_response_body_structure(self):
            self.assertIsInstance(self.response.json()['confidence'], float)
            self.assertIsInstance(self.response.json()['predicted_language'], str)

    def test_response_contains_predicted_language(self):
        jsonData = self.response.json()
        self.assertIsInstance(jsonData['predicted_language'], str)

    def test_response_body_structure_is_correct(self):
        jsonData = self.response.json()
        self.assertIsInstance(jsonData['confidence'], (int, float))
        self.assertIsInstance(jsonData['predicted_language'], str)


    
    
   