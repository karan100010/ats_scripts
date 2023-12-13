import logging
import subprocess

# Get logger with the same name as the main module
logger = logging.getLogger(__name__)


def run_docker_compose_detached(compose_file_path, compose_name):
    """
    Runs Docker Compose in detached mode with the specified compose file.
    Returns True if Docker Compose execution is successful, False otherwise.

    Parameters
    ----------
    compose_file_path : str
        Path to the Docker Compose file

    Returns
    -------
    bool
        True if Docker Compose execution is successful, False otherwise

    """
    try:
        logger.info(f"Running Compose for {compose_name}...")
        logger.info(f"Running Docker Compose in detached mode with file: {compose_file_path}")
        
        # Use subprocess to run docker-compose command
        subprocess.run(["docker-compose", "-f", compose_file_path, "up", "-d"], check=True)

        logger.info("Docker Compose execution initiated in detached mode.")
        logger.info("Please wait for the containers to start...")
        logger.info(f"SUCCESS: Docker Compose execution completed for {compose_name}.")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running Docker Compose for {compose_name}: {e}")
        return False
    except FileNotFoundError:
        logger.error("The 'docker-compose' command is not found. Please make sure Docker Compose is installed.")
        return False
    except Exception as e:
        logger.exception(f"An unexpected error occurred during Docker Compose execution for {compose_name}: {e}")
        return False

