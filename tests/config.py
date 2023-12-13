import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()  # Load variables from .env file

        # Define your variables here
        self.SPACY_API_ENDPOINT = os.getenv("SPACY_API_ENDPOINT")
        


