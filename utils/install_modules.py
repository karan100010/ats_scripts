import sys
import subprocess
import logging

logger = logging.getLogger(__name__)

def get_pip_command():
    """
    Get the correct pip command for the currently running Python interpreter.
    """
    try:
        # Get the path of the currently running Python interpreter
        python_path = sys.executable

        # Use subprocess to run the 'pip' module associated with the Python interpreter
        result = subprocess.run([python_path, "-m", "pip", "--version"], capture_output=True, text=True, check=True)
        print(f"result: {result}")
        # Extract the pip command from the output
        pip_command = result.stdout.split()[0]

        print(f"pip command: {pip_command}")
        return pip_command
    except subprocess.CalledProcessError as e:
        logger.error(f"Error getting the pip command: {e}")
        exit(1)

def run_pip_install():
    """
    Runs pip install for all the modules in the requirements.txt file.
    Returns True if pip install is successful, False otherwise.
    """
    try:
        logger.info("Running pip install for all the modules in the requirements.txt file...")

        # Get the correct pip command for the currently running Python interpreter
        pip_command = get_pip_command()

        # Use subprocess to run pip install command
        subprocess.run([pip_command, "install", "-r", "requirements.txt"], check=True)

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