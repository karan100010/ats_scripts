from dotenv import load_dotenv

import os

load_dotenv()  

class Config():
    def __init__(self):
        self.airflow_compose_path = os.getenv("AIRFLOW_COMPOSE_PATH")
        self.chroma_compose_path = os.getenv("CHROMA_COMPOSE_PATH")
        self.nemo_en_compose_path = os.getenv("NEMO_EN_COMPOSE_PATH")
        self.nemo_hi_compose_path = os.getenv("NEMO_HI_COMPOSE_PATH")
        self.spacy_compose_path = os.getenv("SPACY_COMPOSE_PATH")
        self.speechbrain_compose_path = os.getenv("SPEECHBRAIN_COMPOSE_PATH")

        self.SPACY_API_HOST = os.getenv("SPACY_API_HOST")
        self.SPEECHBRAIN_API_HOST = os.getenv("SPEECHBRAIN_API_HOST")
        self.NEMO_EN_API_HOST = os.getenv("NEMO_EN_API_HOST")
        self.NEMO_HI_API_HOST = os.getenv("NEMO_HI_API_HOST")
        self.CHROMA_API_HOST = os.getenv("CHROMA_API_HOST")
        self.AIRFLOW_API_HOST = os.getenv("AIRFLOW_API_HOST")
        
