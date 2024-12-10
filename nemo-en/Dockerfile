# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Update the package list and install required packages
RUN apt-get update && \
    apt-get install -y libsndfile1 ffmpeg
# Download the Vosk model
RUN wget -O vosk-model-hi-0.22.zip https://alphacephei.com/vosk/models/vosk-model-hi-0.22.zip
RUN wget https://alphacephei.com/vosk/models/vosk-model-en-in-0.5.zip

# Unzip the Vosk model
RUN unzip vosk-model-hi-0.22.zip -d vosk-model && rm vosk-model-hi-0.22.zip
RUN unzip vosk-model-en-in-0.5.zip -d vosk-model && rm vosk-model-en-in-0.5.zip

# Install Cython using pip
RUN pip install --no-cache-dir Cython Flask gunicorn requests pydub vpsk

# Install nemo_toolkit and its dependencies using pip
RUN pip install --no-cache-dir nemo_toolkit['all']
# Expose the necessary port
EXPOSE 5002



# Copy the current directory contents into the container at /app
COPY . /app

# Specify the command to run on container start
CMD ["python", "app.py"]
