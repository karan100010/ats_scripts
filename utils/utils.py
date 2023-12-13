import logging

# Get logger with the same name as the main module
logger = logging.getLogger(__name__)

def check_compose_path(compose_path, compose_name):
    if compose_path is None:
        logger.error(f"{compose_name} environment variable is not set. Please set it to the path of the Docker Compose file.")
        exit(1)
    else:
        logger.info(f"{compose_name} environment variable is set to: {compose_path}")


