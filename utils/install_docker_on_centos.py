import subprocess
import logging

# Configure logging
logging.basicConfig( level=logging.INFO)
logger = logging.getLogger(__name__)

def run_command(command):
    logger.info(f"Running command: {command}")
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return process.returncode, output.decode('utf-8'), error.decode('utf-8')

def is_docker_installed():
    # Check if Docker is installed by running a Docker command
    return_code, _, _ = run_command("docker --version")
    return return_code == 0

def install_docker():
    try:
        logger.info("Starting Docker installation process")

        if is_docker_installed():
            logger.info("Docker is already installed. Skipping installation.")
            return

        # Step 2: Install yum-utils and add the Docker repo
        run_command("sudo yum install -y yum-utils")
        run_command("sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo")

        # Step 3: Install Docker components
        run_command("sudo yum install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin")

        # Start and enable Docker
        run_command("sudo systemctl start docker")
        run_command("sudo systemctl enable docker")

        # Add the current user to the "docker" group to run Docker commands without sudo
        run_command("sudo usermod -aG docker $(whoami)")

        logger.info("Docker has been installed. Please log out and log back in to use Docker without sudo.")

    except Exception as e:
        logger.error(f"Error: {str(e)}")


if __name__ == "__main__":
    install_docker()
