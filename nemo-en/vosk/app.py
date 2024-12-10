from flask import Flask, request, jsonify
from vosk import Model, KaldiRecognizer
import wave
import os

app = Flask(__name__)

# Load the Vosk model
MODEL_PATH = "path/to/vosk-model-en-in-0.5"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("Vosk model not found at the specified path. Please download and place it.")

model = Model(MODEL_PATH)

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    """
    Endpoint to transcribe audio using Vosk.
    Expects a .wav file as input.
    """
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    try:
        # Open and read the WAV file
        with wave.open(audio_file, 'rb') as wf:
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [8000, 16000, 32000, 48000]:
                return jsonify({"error": "Invalid audio format. Ensure mono WAV at 8k, 16k, 32k, or 48k Hz"}), 400

            # Initialize recognizer with sample rate
            rec = KaldiRecognizer(model, wf.getframerate())
            rec.SetWords(True)

            transcription = ""
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    transcription += rec.Result()

            transcription += rec.FinalResult()

        return jsonify({"transcription": transcription}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to process audio: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
