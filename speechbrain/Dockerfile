FROM python:3.9

WORKDIR /speechbrain

# Install necessary dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Copy the "app.py" file into the "speechbrain" folder
COPY ./app.py /speechbrain


# Expose the necessary port
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
