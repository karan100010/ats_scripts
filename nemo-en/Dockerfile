# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Update the package list and install required packages
RUN apt-get update && \
    apt-get install -y libsndfile1 ffmpeg

# Install Cython using pip
RUN pip install --no-cache-dir Cython Flask gunicorn requests pydub

# Install nemo_toolkit and its dependencies using pip
RUN pip install --no-cache-dir nemo_toolkit['all']
# Expose the necessary port
EXPOSE 5002



# Copy the current directory contents into the container at /app
COPY . /app

# Specify the command to run on container start
CMD ["python", "app.py"]
