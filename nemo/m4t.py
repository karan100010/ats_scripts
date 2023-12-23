import torchaudio
from transformers import AutoProcessor, SeamlessM4TModel
from flask import Flask, request, jsonify
import json
import os
import sys
import librosa

app = Flask(__name__)

# Load the language identification model

processor = AutoProcessor.from_pretrained("facebook/hf-seamless-m4t-medium")
model = SeamlessM4TModel.from_pretrained("facebook/hf-seamless-m4t-medium")
# read output.wav 

@app.route('/api_status', methods=['GET'])
def api_status():
    return jsonify({
        "status": "ok", 
        "message":"speechbrain is up and running"
        }), 200
@app.route('/get_translation', methods=['GET'])
def get_translation():
     audio_input, _ = torchaudio.load("outputx.wav")
    inputs = processor(audio_data, sampling_rate=16_000, return_tensors="pt")
    audio_sample = model.generate(**inputs)
    audio_inputs = processor(audios=audio_sample["array"], return_tensors="pt")
    output_tokens = model.generate(**audio_inputs, tgt_lang="eng", generate_speech=False)
    translated_text_from_audio = processor.decode(output_tokens[0].tolist()[0], skip_special_tokens=True)
    return jsonify({
        "status": "ok", 
        "message": translated_text_from_audio
        }), 200

if __name__ == '__main__':
    #run on port 5006
    app.run(host='localhost', port=5006)




