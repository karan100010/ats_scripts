from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
import vosk
import json

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Load Vosk models
asr_model_en = vosk.Model("/fra/KARAN/vosk-model-en-in-0.5/vosk-model-en-in-0.5")
asr_model_hi = vosk.Model("/fra/KARAN/vosk-model-hi-0.22")


# Create recognizers for English and Hindi
recognizer_en = vosk.KaldiRecognizer(asr_model_en, 8000)
recognizer_hi = vosk.KaldiRecognizer(asr_model_hi, 8000)


# SocketIO namespace for WebRTC audio streaming
@app.route('/')
def index():
    return "WebRTC Speech Recognition API is running."


# WebSocket endpoint for English ASR
@socketio.on('audio_en')
def handle_audio_en(audio_data):
    if recognizer_en.AcceptWaveform(audio_data):
        result = recognizer_en.Result()
    else:
        result = recognizer_en.PartialResult()
    emit('asr_result', json.loads(result))


# WebSocket endpoint for Hindi ASR
@socketio.on('audio_hi')
def handle_audio_hi(audio_data):
    if recognizer_hi.AcceptWaveform(audio_data):
        result = recognizer_hi.Result()
    else:
        result = recognizer_hi.PartialResult()
    emit('asr_result', json.loads(result))


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5003)
