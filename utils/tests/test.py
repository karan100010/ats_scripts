from .spacy.api_test import  APIStatusTest as SpacyAPIStatusTest, GETEntitiesTest as SpacyGETEntitiesTest 
from .speechbrain.api_test import APIStatusTest as SpeechBrainAPIStatusTest, PredictLanguage as SpeechbrainPredictLanguage
from .chroma.api_test import  APIStatusTest as ChromaAPIStatusTest
from .nemo_hi.api_test import APITestCase as NemoHiAPITestCase, TranscribeHi as NemoHiTranscribeHi
from .nemo_en.api_test import APITestCase as NemoEnAPITestCase, TranscribeEn as NemoEnTranscribeEn
from .airflow.api_test import APIStatusTest as AirflowAPIStatusTest
import unittest



def run_tests():

    loader = unittest.TestLoader()
    
    # spacy suite
    spacy_api_status_suite = loader.loadTestsFromTestCase(SpacyAPIStatusTest)
    spacy_get_entities_suite = loader.loadTestsFromTestCase(SpacyGETEntitiesTest)

    # spacy suite
    speechbrain_api_status_suite = loader.loadTestsFromTestCase(SpeechBrainAPIStatusTest)
    speechbrain_predict_language_suite = loader.loadTestsFromTestCase(SpeechbrainPredictLanguage)

    # Chroma suite
    chroma_api_status_suite = loader.loadTestsFromTestCase(ChromaAPIStatusTest)

    # Nemo Hindi suite
    nemo_hi_api_status_suite = loader.loadTestsFromTestCase(NemoHiAPITestCase)
    nemo_hi_api_transcribe = loader.loadTestsFromTestCase(NemoHiTranscribeHi)

    # Nemo English suite
    nemo_en_api_status_suite = loader.loadTestsFromTestCase(NemoEnAPITestCase)
    nemo_en_api_transcribe = loader.loadTestsFromTestCase(NemoEnTranscribeEn)

    # Nemo English suite
    airflow_api_status_suite = loader.loadTestsFromTestCase(AirflowAPIStatusTest)


    # Combine the two suites
    combined_suite = unittest.TestSuite([
        spacy_api_status_suite, 
        spacy_get_entities_suite, 
        speechbrain_api_status_suite, 
        speechbrain_predict_language_suite,
        chroma_api_status_suite,
        nemo_hi_api_status_suite,
        nemo_hi_api_transcribe,
        nemo_en_api_status_suite,
        nemo_en_api_transcribe,
        airflow_api_status_suite
        ])


    runner = unittest.TextTestRunner()
    result = runner.run(combined_suite)

    if result.wasSuccessful():
        print("All tests ran successfully.")
    else:
        print("Some tests failed.")





