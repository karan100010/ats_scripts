import subprocess
import sounddevice as sd
import numpy as np
import webrtcvad

# Parameters for audio streaming
channels = 1
sample_rate = 16000  # You may need to adjust this based on your audio source

# Parameters for VAD
vad = webrtcvad.Vad()
vad.set_mode(3)  # Aggressiveness mode (0 to 3)

# Variables for noise detection
noise_frames_threshold = int(2 * sample_rate / 512)  # 2 seconds
noise_frames_count = 0

# Function to detect noise
def detect_noise(indata, frames, time, status):
    global noise_frames_count

    # Convert the audio data to 16-bit integers
    samples = np.frombuffer(indata, dtype=np.int16)
    
    # Perform noise detection using VAD
    is_noise = vad.is_speech(samples.tobytes(), sample_rate)

    if is_noise:
        noise_frames_count += frames
    else:
        noise_frames_count = 0

    # If noise is detected for more than the threshold, take action
    if noise_frames_count >= noise_frames_threshold:
        print("Noise detected for more than 2 seconds! Taking action.")
        sd.stop()

#use Audiosocket protocal to read audio data
#start audio streaming with the noise detection callback
        
 