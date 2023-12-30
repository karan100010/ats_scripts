#!/usr/bin/env python

import sys
from pydub import AudioSegment

def detect_silence(audio, silence_threshold=-40.0, silence_duration=500):
    silence_segments = []
    chunk_size = 10  # milliseconds

    for i in range(0, len(audio), chunk_size):
        chunk = audio[i:i + chunk_size]
        if chunk.dBFS < silence_threshold:
            if not silence_segments:
                start_time = i
            silence_segments.append(chunk)
        else:
            if silence_segments and len(silence_segments) * chunk_size >= silence_duration:
                end_time = i
                silence_segments = []
                yield start_time, end_time

def main():
    try:
        # Read ulaw-encoded audio from stdin
        ulaw_data = sys.stdin.buffer.read()

        # Convert ulaw to a standard format (e.g., WAV) for easier processing
        ulaw_audio = AudioSegment(ulaw_data, frame_rate=8000, sample_width=2, channels=1)
        
        # Detect silence segments
        silence_segments = list(detect_silence(ulaw_audio))

        # Print detected silence segments
        for start_time, end_time in silence_segments:
            print(f"Silence segment: {start_time} ms - {end_time} ms")

    except Exception as e:
        sys.stderr.write(str(e))

if __name__ == "__main__":
    main()

