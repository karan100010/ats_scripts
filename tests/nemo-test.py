from locust import HttpUser, task, between
from functions import load_speechbrain_csv, count_syllables, get_audio_length_from_url
import random
import os
import numpy as np

class LanguagePredictionUser(HttpUser):
    wait_time = between(0.5,2)
    host = os.environ.get("SPEECHBRAIN_API_HOST", "http://localhost:5000")
    audio_files = load_speechbrain_csv("./data/speechbrain.csv")
    threshold = 1.0

    response_times = []
    time_by_audio_len = []

    def on_start(self):
        # This method is called when a new user is starting a task
        self.audiofile = random.choice(self.audio_files)

    @task
    def transcribe_hi(self):

        data = {"audiofile": self.audiofile}  
        headers = {"Content-Type": "application/json"} 

        self.audio_length = get_audio_length_from_url(self.audiofile)       
        print(f"Audio length: {self.audio_length:.4f} seconds")
    
        with self.client.post("/transcribe_hi", json=data, headers=headers, catch_response=True) as response:
            # Log the response time and other metrics
            self.log_response(response)

    @task
    def transcribe_hi(self):

        data = {"audiofile": self.audiofile}  
        headers = {"Content-Type": "application/json"} 

        self.audio_length = get_audio_length_from_url(self.audiofile)       
        print(f"Audio length: {self.audio_length:.4f} seconds")
    
        with self.client.post("/transcribe_hi", json=data, headers=headers, catch_response=True) as response:
            # Log the response time and other metrics
            self.log_response(response)
        
    def log_response(self, response):
        print(f"Response status code: {response.status_code}")
        print(f"Response text: {response.text}")
        
        # Append response time to the list for further analysis
        self.response_times.append(response.elapsed.total_seconds())

        # Use the custom metric for further calculations or analysis
        self.log_response_time(response.elapsed.total_seconds())


        time_by_audio_len = response.elapsed.total_seconds() / self.audio_length
        print(f"Time by len_audio: {time_by_audio_len:.4f} seconds")
        self.time_by_audio_len.append(time_by_audio_len)

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
            median_time_by_audio_len = np.median(self.time_by_audio_len)
            print(f"Median Time by audio len: {median_time_by_audio_len:.4f} seconds")

            # Calculate and print 95th percentile response time
            percentile_95_response_time = np.percentile(self.response_times, 95)
            print(f"95th Percentile Response Time: {percentile_95_response_time:.4f} seconds")

            # Calculate and print 95th percentile time per syllable
            percentile_95_time_by_audio_len = np.percentile(self.time_by_audio_len, 95)
            print(f"95th Percentile Time by audio len: {percentile_95_time_by_audio_len:.4f} seconds")
            
            # Print count of failed requests
            requests_exceeding_threshold_time = len([time for time in self.response_times if time > self.threshold])
            print(f"Failed Requests: {requests_exceeding_threshold_time}")


