from utils import install_docker_on_centos
from utils.install_modules import run_pip_install
from utils.docker_utils import run_docker_compose_detached
from utils.utils import check_compose_path
from dotenv import load_dotenv
import os

from config import Config

from utils.tests import test
import logging as logger


config = Config()

# Load environment variables from .env file
load_dotenv()

# Configure logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

if __name__ == '__main__':
    # Install Docker on CentOS
    # install_docker_on_centos.install_docker()
    
    # Run pip install for all the modules in the requirements.txt file
    # run_pip_install()

    # # Get ENV variables
    airflow_compose_path = config.airflow_compose_path
    # chroma_compose_path = config.chroma_compose_path
    # nemo_en_compose_path = config.nemo_en_compose_path
    # nemo_hi_compose_path = config.nemo_hi_compose_path
    # spacy_compose_path = config.spacy_compose_path
    # speechbrain_compose_path = config.speechbrain_compose_path

    # # # Check if the environment variables are set for all the Docker Compose files
    # check_compose_path(airflow_compose_path, "AIRFLOW_COMPOSE_PATH")
    # check_compose_path(chroma_compose_path, "CHROMA_COMPOSE_PATH")
    # check_compose_path(nemo_en_compose_path, "NEMO_EN_COMPOSE_PATH")
    # check_compose_path(nemo_hi_compose_path, "NEMO_hi_COMPOSE_PATH")
    # check_compose_path(spacy_compose_path, "SPACY_COMPOSE_PATH")
    # check_compose_path(speechbrain_compose_path, "SPEECHBRAIN_COMPOSE_PATH")
    

    # # Run Docker Compose in detached mode
    # run_docker_compose_detached(airflow_compose_path, "Airflow")
    # run_docker_compose_detached(chroma_compose_path, "Chroma")
    # run_docker_compose_detached(nemo_en_compose_path, "NEMO_EN")
    # run_docker_compose_detached(nemo_hi_compose_path, "NEMO_hi")
    # run_docker_compose_detached(spacy_compose_path, "Spacy")
    # run_docker_compose_detached(speechbrain_compose_path, "Speechbrain")
    


    # Run tests
    test.run_tests()

    
