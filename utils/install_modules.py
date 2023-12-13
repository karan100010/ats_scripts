import subprocess
import logging

logger = logging.getLogger(__name__)

def run_pip_install():
    """
    Runs pip install for all the modules in the requirements.txt file.
    Returns True if pip install is successful, False otherwise.

    Returns
    -------
    bool
        True if pip install is successful, Exits otherwise

    """
    try:
        logger.info("Running pip install for all the modules in the requirements.txt file...")
        # Use subprocess to run pip install command
        subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
        logger.info("SUCCESS: pip install completed for all the modules in the requirements.txt file.")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running pip install for all the modules in the requirements.txt file: {e}")        
        exit(1)
    except FileNotFoundError:
        logger.error("The 'pip' command is not found. Please make sure pip is installed.")
        exit(1)
    except Exception as e:
        logger.exception(f"An unexpected error occurred during pip install for all the modules in the requirements.txt file: {e}")
        exit(1)