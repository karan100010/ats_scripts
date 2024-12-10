from flask import Flask, request, jsonify
from datetime import datetime
#import nemo.collections.asr as nemo_asr

import vosk

#import nemo.collections.nlp as nemo_nlp


app = Flask(__name__)

asr_model_en=vosk.Model("/fra/KARAN/vosk-model-en-in-0.5/vosk-model-en-in-0.5")
#asr_model_hi=vosk.Model("vosk-model/vosk-model-hi-0.22")
#recognizer_hi = vosk.KaldiRecognizer(asr_model_hi, 8000)
recognizer_en = vosk.KaldiRecognizer(asr_model_en, 8000)

@app.route('/vosk_hi', methods=['POST'])

def convert_ulaw_to_wave():
     recognizer_hi = recognizer_hi.AcceptWaveform(request.get_data())
     result = recognizer_hi.FinalResult()
     return jsonify(result)

@app.route('/vosk_hi', methods=['POST'])

def convert_ulaw_to_wave():
     recognizer_en = recognizer_en.AcceptWaveform(request.get_data())
     result = recognizer_en.FinalResult()
     return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003) 
    

     

