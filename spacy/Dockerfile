FROM python:3.9-slim 

WORKDIR /spacy

# Install necessary dependencies
COPY requirements.txt .
COPY requirements-intent.txt .  
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements-intent.txt

# RUN python -m spacy download en_core_web_trf


# Copy the "app.py" file into the "speechbrain" folder
COPY ./app.py /spacy
COPY ./functions.py /spacy
COPY ./model-2/ /spacy/model
RUN ls -l model/


# Expose the necessary port
EXPOSE 5001

# Command to run the application
CMD ["python", "app.py"]
