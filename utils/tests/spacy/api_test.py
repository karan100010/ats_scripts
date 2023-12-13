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
        self.API_ENDPOINT = config.SPACY_API_ENDPOINT + self.get_endpoint()

    def get_endpoint(self):
        raise NotImplementedError("Subclasses must implement get_endpoint method.")

    def test_status_code_is_200(self):
        response = requests.get(self.API_ENDPOINT)
        self.assertEqual(int(response.status_code), 200)

    def test_response_is_json(self):
        response = requests.get(self.API_ENDPOINT)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

    def test_response_time_less_than_200ms(self):
        response = requests.get(self.API_ENDPOINT)
        self.assertLess(response.elapsed.total_seconds() * 1000, 200)

    
    


class APIStatusTest(APITestCase):

    def get_endpoint(self):
        return "/api_status"

    def test_response_body_not_empty(self):
        json_data = self.get_json_data()
        self.assertTrue(json_data.get('message'))
        self.assertTrue(json_data.get('status'))

    def test_response_contains_status_value(self):
        json_data = self.get_json_data()
        self.assertIsInstance(json_data.get('status'), str)

    def test_response_body_structure_correct(self):
        json_data = self.get_json_data()
        self.assertIsInstance(json_data.get('status'), str)

    def get_json_data(self):
        response = requests.get(self.API_ENDPOINT)
        return response.json()
    


class GETEntitiesTest(APITestCase):

    def get_endpoint(self):
        return "/get_entities"

    def test_entity_information_present(self):
        json_data = self.get_json_data()
        self.assertIsInstance(json_data, list)

    def test_response_body_structure(self):
        json_data = self.get_json_data()
        for item in json_data:
            self.assertIsInstance(item['entity'], str)
            self.assertIsInstance(item['text'], str)
            self.assertIsInstance(item['label'], str)

    def get_json_data(self):
        data = {
            "sentence": "yes saqib shah is me"
        }
        headers={"Content-Type": "application/json"}
        
        response = requests.post(self.API_ENDPOINT, json=data, headers=headers)

        print("RESPONSE: ",response.status_code)
        return response.json()
    
   