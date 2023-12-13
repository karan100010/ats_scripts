from .spacy.api_test import  APIStatusTest, GETEntitiesTest
import unittest



def run_tests(config):

    loader = unittest.TestLoader()
    api_status_suite = loader.loadTestsFromTestCase(APIStatusTest)
    get_entities_suite = loader.loadTestsFromTestCase(GETEntitiesTest)

    # Combine the two suites
    combined_suite = unittest.TestSuite([api_status_suite, get_entities_suite])


    runner = unittest.TextTestRunner()
    result = runner.run(combined_suite)

    if result.wasSuccessful():
        print("All tests ran successfully.")
    else:
        print("Some tests failed.")

    # test = APIStatusTest(config)
    # test.test_response_is_json()
    # test.test_status_code_is_200()
    # test.test_response_time_less_than_200ms()
    # test.get_json_data()
    # test.test_response_body_not_empty()
    # test.test_response_contains_status_value()
    # test.test_response_body_structure_correct()



