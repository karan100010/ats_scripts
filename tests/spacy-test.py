from locust import HttpUser, task, between, events, constant
import random
import os
import numpy as np
from functions import count_syllables, load_spacy_csv



class EntityExtraction(HttpUser):
    wait_time = between(0.5, 2)
    host = os.environ.get("SPACY_API_HOST", "http://localhost:5001")
    threshold = 1.0
    sentences = load_spacy_csv("./data/spacy.csv")



    response_times = []
    time_per_syllable = []

    def on_start(self):
        # This method is called when a new user is starting a task
        self.sentence = random.choice(self.sentences)
        wait_time = between(5, 6)

    @task
    def get_entities(self):
        data = {"sentence": self.sentence}
        headers = {"Content-Type": "application/json"}

        # Make a POST request to /get_entities
        with self.client.post("/get_entities", json=data, headers=headers, catch_response=True) as response:
            # Log the response time and other metrics
            self.log_response(response)

    def log_response(self, response):
        # Log the response details (customize as needed)
        print(f"Response status code: {response.status_code}")
        print(f"Response text: {response.text}")

        # Append response time to the list for further analysis
        self.response_times.append(response.elapsed.total_seconds())

        # Use the custom metric for further calculations or analysis
        self.log_response_time(response.elapsed.total_seconds())

        time_per_syllable = response.elapsed.total_seconds() / count_syllables(self.sentence)
        print(f"Time per syllable: {time_per_syllable:.4f} seconds")
        self.time_per_syllable.append(time_per_syllable)

    
    
    def log_response_time(self, response_time):
        # Example: Determine if the response time is above a certain threshold
          # Adjust the threshold as needed
        if response_time > self.threshold:
            print("Warning: Response time is higher than the threshold.")
        else:
            print("Response time is within acceptable limits.")

        
    def on_stop(self):
        # This method is called when a user stops their tasks
        # Calculate and print summary metrics
        self.print_summary_metrics()

    def print_summary_metrics(self):
        if self.response_times:
            # Calculate and print median response time
            median_response_time = np.median(self.response_times)
            print(f"Median Response Time: {median_response_time:.4f} seconds")

            # Calculate and print median time per syllable
            median_time_per_syllable = np.median(self.time_per_syllable)
            print(f"Median Time per Syllable: {median_time_per_syllable:.4f} seconds")

            # Calculate and print 95th percentile response time
            percentile_95_response_time = np.percentile(self.response_times, 95)
            print(f"95th Percentile Response Time: {percentile_95_response_time:.4f} seconds")

            # Print count of failed requests
            requests_exceeding_threshold_time = len([time for time in self.response_times if time > self.threshold])
            print(f"Failed Requests: {requests_exceeding_threshold_time}")
