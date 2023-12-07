
import csv
import requests
from pydub import AudioSegment
from io import BytesIO
import os
import random


def read_csv_to_list(file_path):
    """
    Read a CSV file and convert it to a list of lists.

    Args:
    - file_path (str): The path to the CSV file.

    Returns:
    list: A list of lists representing the data from the CSV file.

    Example:
    >>> csv_file_path = "example.csv"
    >>> data_list = read_csv_to_list(csv_file_path)
    >>> print(data_list)
    [['Header1', 'Header2', 'Header3'], ['Value1', 'Value2', 'Value3'], ...]
    """
    data_list = []
    with open(file_path, mode="r") as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            data_list.append(row)
    return data_list


def load_spacy_csv(filepath):
    data_list = read_csv_to_list(filepath)

    # Remove the header row
    data = data_list.pop(0)
    # find the index of the sentence column
    sentence_index = data.index("sentences")
    sentences = [row[sentence_index] for row in data_list] 
    return sentences

def load_speechbrain_csv(filepath):
    data_list = read_csv_to_list(filepath)

    # Remove the header row
    data = data_list.pop(0)
    # find the index of the sentence column
    audio_files_index = data.index("audio_files")
    audio_files = [row[audio_files_index] for row in data_list] 
    return audio_files


def count_syllables(word):
    """
    Count the number of syllables in a word using a basic heuristic.

    Args:
    - word (str): The word for which syllables need to be counted.

    Returns:
    - int: The number of syllables in the word.
    """
    vowels = "aeiouy"
    count = 0
    prev_char_was_vowel = False

    for char in word.lower():
        if char in vowels:
            if not prev_char_was_vowel:
                count += 1
            prev_char_was_vowel = True
        else:
            prev_char_was_vowel = False

    return count


def download_file_temp(url):
    """
    Download a file from a URL and save it to a temporary file.

    Args:
    - url (str): The URL of the file to download.

    Returns:
    - str: The path to the temporary file.
    """
    response = requests.get(url, stream=True)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Use BytesIO to create a file-like object from the binary data
        file_data = BytesIO(response.content)
        
        # Save the file data to a temporary file
        random_number = random.randint(0, 1000000)
        temp_filename = f"temp_file_{random_number}.wav"
        file = open(temp_filename, "wb")
        file.write(file_data.read())
        file.close()

        temp_filename = os.path.abspath(temp_filename)
        
        return temp_filename
    else:
        # Print an error message if the request was not successful
        print(f"Failed to fetch file from {url}. Status code: {response.status_code}")
        return None
    



def get_audio_length(file_path):
        """
        Get the length of an audio file in seconds.
        
        Args:
        - file_path (str): The path to the audio file.

        Returns:
        - float: The length of the audio file in seconds.
        
        """

        # 
        audio = AudioSegment.from_file(file_path)
        length_in_seconds = len(audio) / 1000.0  # Convert milliseconds to seconds
        return length_in_seconds



def get_audio_length_from_url(url):
    """
    Download an audio file from a URL and get its length in seconds.
    
    Args:
    - url (str): The URL of the audio file.

    Returns:
    - float: The length of the audio file in seconds.
    
    """

    
    # Download the file to a temporary file
    temp_filename = download_file_temp(url)
    
    # Get the length of the audio file
    length_in_seconds = get_audio_length(temp_filename)
    
    # Delete the temporary file
    os.remove(temp_filename)
    
    return length_in_seconds
