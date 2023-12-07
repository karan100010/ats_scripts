# Load Testing Documentation

# Table of Contents

1. [Overview](#overview)
2. [Load Testing Tool](#load-testing-tool)
   - [Setup Instructions](#setup-instructions)
3. [Test Configuration](#test-configuration)
   - [System Specifications](#system-specifications)
   - [Load Testing Configuration](#load-testing-configuration)
4. [Testing Spacy Entity Extraction](#testing-spacy-entity-extraction)
   - [Endpoints Tested](#endpoints-tested)
   - [How to Run the Load Test](#how-to-run-the-load-test)
   - [Data Usage Information](#data-usage-information)
     - [Data Format](#data-format)
     - [Note](#note)
   - [Metrics](#metrics)
   - [Observations](#observations)
     - [Metrics Recorded](#metrics-recorded)
   - [Conclusion](#conclusion)
   - [Additional Resources](#additional-resources)
5. [Testing Speechbrain Language Identification](#testing-speechbrain-language-identification)
   - [Endpoints Tested](#endpoints-tested-1)
   - [How to Run the Load Test](#how-to-run-the-load-test-1)
   - [Data Usage Information](#data-usage-information-1)
     - [Data Format](#data-format-1)
     - [Note](#note-1)
   - [Metrics](#metrics-1)
   - [Observations](#observations-1)
     - [Metrics Recorded](#metrics-recorded-1)
   - [Conclusion](#conclusion-1)
   - [Additional Resources](#additional-resources-1)

## Overview

The purpose of this load testing is to evaluate the performance of the following Docker containers:

1. Testing Spacy Entity Extraction
2. Testing Speechbrain Language Identification
3. Testing Nemo

Each container will be tested individually to assess its scalability and responsiveness under load.

## Load Testing Tool

For this load testing, we are using [Locust](https://locust.io/), a Python-based open-source load testing tool. Locust allows you to define user behavior with Python code, making it highly customizable for various testing scenarios.

### Setup Instructions

To run the load tests with Locust, follow these setup instructions:

1. Install Locust and its dependencies:

   ```bash
   # Install dependencies
   pip install locust pydub numpy
   ```

## Test Configuration

### System Specifications

- **Processor**: 12th Gen Intel(R) Core(TM) i5-12500H @ 2.50 GHz
- **Installed RAM**: 16.0 GB (15.6 GB usable)
- **System type**: 64-bit operating system, x64-based processor

- **Dedicated Graphics**:
  Na

### Load Testing Configuration

- **Number of Users**: 10
- **Duration of the Test**: 15 minutes

## Testing Spacy Entity Extraction

### Endpoints Tested

    1. /get_entities

### How to Run the Load Test

1. Navigate to the `/tests` directory in the `ats_scripts` repo

```bash
cd ./tests
```

2. Run the following command to run the test for spacy.
   Note: Make sure the spacy container is running on the port `5001`

```bash
# Command to run the Locust test
locust -f spacy-test.py
```

Alternatively you can create an `.env` file to set the host for the spacy server.

```env
<!-- ENV FILE -->
SPACY_API_HOST=http://localhost:5001
```

## Data Usage Information

The data used for evaluating the model is stored in the `./data/spacy.csv` file.

### Data Format

The dataset follows a single-column CSV format with the header named `sentences`. Each row contains a sentence that serves as input for accessing the model.

#### Example:

```csv
sentences
This is a sample sentence.
Another example for testing.
...
```

### Note

Please be aware that the current dataset, as indicated by the note, may need improvement. It is advisable to review and enhance the dataset to ensure it adequately represents the diversity of scenarios and language patterns that the model is expected to handle. Continuous refinement of the dataset will contribute to the model's robustness and effectiveness in real-world scenarios.

### Metrics

Document the key metrics you collected during the load test. Include metrics like:

- Requests per second: Number of requests per second
- Response time: Response time to fullfill the task by the entity extraction endpoint
- Response time per Syllable: Response time divided by the number of Syllables in the sentence.

Note: The function to count the number of Syllables is a basic heuristic present in `./functions.py`. This can be switched up with a better function to produce better results.

### Observations:

#### Metrics Recorded

| Metric                            | Endpoint      | Value    |
| --------------------------------- | ------------- | -------- |
| Requests per second               | /get_entities | 7.4      |
| Median response time              | /get_entities | 71.8 ms  |
| 95th percentile                   | /get_entities | 143.2 ms |
| Median response time per Syllable | /get_entities | 5.6 ms   |

1. **Requests per Second (RPS):**

   - The system is handling approximately 7.4 requests per second. This metric indicates the throughput of the system under the given load.

2. **Median Response Time:**

   - The median response time of 71.8 ms suggests that 50% of the requests are processed within this time frame. This is a key indicator of the system's responsiveness.

3. **95th Percentile Response Time:**

   - The 95th percentile response time of 143.2 ms is crucial for understanding the behavior of the system under varying load conditions. It represents the response time experienced by the majority of users and can highlight potential performance issues during peak usage.

4. **Median Response Time per Syllable:**
   - The low median response time per syllable of 5.6 ms indicates efficient processing of individual syllables, suggesting the model's capability for quick and consistent handling of sentences of varying lengths.

### Conclusion

Key findings from the load test:

1. **Throughput (RPS):**

   - System handles 7.4 requests per second, indicating moderate capacity.

2. **Responsiveness:**

   - Median response time is 71.8 ms. Consider optimization for stricter performance goals.

3. **Percentile Response Times:**

   - 95th percentile is 143.2 ms, addressing the majority of users. Optimize for enhanced user satisfaction.

4. **Efficient Syllable Processing:**
   - Low median response time per syllable (5.6 ms) demonstrates consistent entity extraction across varying sentence lengths. Though more robust testing is required after updating the dataset used for this test.

### Additional Resources

Here are some additional resources that may be helpful for understanding or reproducing the load test:

1. [Spacy Documentation](https://spacy.io/documentation): Refer to the official Spacy documentation for information on using Spacy for natural language processing tasks, including entity extraction.

2. [Docker Documentation](https://docs.docker.com/): Explore Docker documentation for details on containerization, managing Docker containers, and deploying applications using Docker.

3. [Locust Documentation](https://docs.locust.io/): Visit the Locust documentation for guidance on setting up and running load tests using Locust, a Python-based open-source load testing tool.

4. [Python Locust GitHub Repository](https://github.com/locustio/locust): Access the GitHub repository for Python Locust to stay updated on the latest releases, contribute to the project, or report issues.

## Testing Speechbrain Language Identification

### Endpoints Tested

    1. /predict_language

### How to Run the Load Test

1. Navigate to the `/tests` directory in the `ats_scripts` repo

```bash
cd ./tests
```

2. Run the following command to run the test for spacy.
   Note: Make sure the spacy container is running on the port `5001`

```bash
# Command to run the Locust test
locust -f speechbrain-test.py
```

Alternatively you can create an `.env` file to set the host for the spacy server.

```env
<!-- ENV FILE -->
SPEECHBRAIN_API_HOST=http://localhost:5000
```

## Data Usage Information

The data used for evaluating the model is stored in the `./data/speechbrain.csv` file.

### Data Format

The dataset follows a single-column CSV format with the header named `audio_files`. Each row contains a url to an audio which is given as input to the language identification model.

#### Example:

```csv
sentences
This is a sample sentence.
Another example for testing.
...
```

### Note

Please be aware that the current dataset, as indicated by the note, may need improvement. It is advisable to review and enhance the dataset to ensure it adequately represents the diversity of scenarios and language patterns that the model is expected to handle. Continuous refinement of the dataset will contribute to the model's robustness and effectiveness in real-world scenarios.

### Metrics

Document the key metrics you collected during the load test. Include metrics like:

- Requests per second: Number of requests per second
- Response time: Response time to fullfill the task by the entity extraction endpoint
- Response time by audio length: Response time divided by the duration of the audio clip.

Note: The function to get the length of the audio is present in `./functions.py`. This can be switched up with a better function to produce better results.

### Observations:

#### Metrics Recorded

| Metric                               | Endpoint          | Value     |
| ------------------------------------ | ----------------- | --------- |
| Requests per second                  | /predict_language | 3         |
| Median response time                 | /predict_language | 840.4 ms  |
| 95th Percentile Response Time        | /predict_language | 1227.1 ms |
| Median Response time by audio length | /predict_language | 0.5413 ms |
| 95th Percentile time by audio length | /predict_language | 860.3 ms  |

### Observations for Language Identification from Audio

1. **RPS and Throughput:**

   - The system handles a moderate throughput of approximately 3 requests per second, suggesting a functional capacity that may warrant scalability examination.

2. **Median Response Time:**

   - A median response time of 840.4 ms reveals a noticeable delay in processing language identification requests, prompting further investigation for potential latency optimizations.

3. **95th Percentile Response Time:**

   - The 95th percentile response time of 1227.1 ms signifies elevated response times for a significant portion of requests. Optimizing for this metric is vital, particularly for real-time or time-sensitive applications.

4. **Response Time by Audio Length:**

   - The efficient median response time by audio length (0.5413 ms) is a positive indicator for audio processing tasks, specifically language identification. This suggests quick processing relative to the audio length.

5. **95th Percentile Time by Audio Length:**
   - The 95th percentile time by audio length (860.3 ms) aligns with general response time observations. Focusing on optimizing audio length-related processing can enhance overall system performance.

### Conclusion

The load test revealed:

1. **Throughput and Response Times:**

   - Moderate throughput of 3 requests per second, but a notable delay with a median response time of 840.4 ms.

2. **Latency Optimization:**

   - Investigation needed for optimizing response times, enhancing system responsiveness for better user experiences.

3. **Efficient Audio Length Processing:**

   - Strong performance in processing audio length, with a positive median response time of 0.5413 ms.

4. **Scalability and Failed Requests:**
   - Address scalability and failed requests (627 due to overtime) for improved system reliability.

### Additional Resources

Here are additional resources for further exploration and understanding of the technologies used in the Language Identification from Audio system:

1. [SpeechBrain Documentation](https://speechbrain.github.io/): Explore the official documentation for SpeechBrain, an open-source speech toolkit. This resource provides detailed information on using SpeechBrain for various audio processing tasks, including language identification.

2. [Locust Documentation](https://docs.locust.io/): Visit the Locust documentation for comprehensive guidance on setting up and running load tests using Locust. This Python-based open-source tool is utilized for load testing and performance analysis.

3. [Docker Documentation](https://docs.docker.com/): Dive into Docker documentation for in-depth insights into containerization, managing Docker containers, and deploying applications using Docker. Docker is a crucial component for packaging and running applications in a consistent environment.

4. [Python Locust GitHub Repository](https://github.com/locustio/locust): Access the GitHub repository for Python Locust to stay updated on the latest releases, contribute to the project, or report issues.
