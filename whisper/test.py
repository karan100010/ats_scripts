import whisper
import sys
import json
import io
import numpy as np
import soundfile as sf
import torch

# Check if CUDA is available
device = "cuda" if torch.cuda.is_available() else "cpu"

def main():
    # Load the Whisper medium model
    model = whisper.load_model("medium",device=device)

    # Check if a file path is provided as a command-line argument
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
        # Load the audio file using Whisper's utility function
        audio = whisper.load_audio(audio_file)
    else:
        # Read 16-bit PCM stream from stdin
        pcm_data = sys.stdin.buffer.read()
        # Create a file-like object from the PCM data
        pcm_file = io.BytesIO(pcm_data)
        # Read the PCM data using soundfile
        # Assuming mono audio, 16 kHz sample rate, and 16-bit depth
        data, samplerate = sf.read(
            pcm_file,
            channels=1,
            samplerate=16000,
            format='RAW',
            subtype='PCM_16'
        )
        audio = data

    # Perform transcription with language detection
    result = model.transcribe(audio, task="transcribe", language=None)

    # Extract language and transcription from the result
    language = result['language']
    transcription = result['text']

    # Prepare the JSON object
    output = {
        "language": language,
        "transcription": transcription
    }

    # Output the JSON
    print(json.dumps(output, ensure_ascii=False))

if __name__ == "__main__":
    main()
