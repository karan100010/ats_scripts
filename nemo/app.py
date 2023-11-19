from flask import Flask, request, jsonify
from datetime import datetime
import nemo.collections.asr as nemo_asr

app = Flask(__name__)

# Load the Hindi ASR model
asr_model_hi = nemo_asr.models.EncDecCTCModelBPE.from_pretrained(model_name="stt_hi_conformer_ctc_medium")

# Load the English ASR model
asr_model_en = nemo_asr.models.EncDecRNNTBPEModel.from_pretrained("nvidia/stt_en_conformer_transducer_xlarge")
import requests
from pydub import AudioSegment
from io import BytesIO

def load_audio_from_url(url):
    # Make a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Get the audio content from the response
        audio_content = BytesIO(response.content)

        # Use pydub to load the audio
        audio = AudioSegment.from_file(audio_content)

        return audio
    else:
        print(f"Failed to fetch audio from {url}. Status code: {response.status_code}")
        return None
    
@app.route('/transcribe_hi', methods=['POST'])
def transcribe_hi():
    if 'audiofile_path' not in request.form:
        return jsonify({'error': 'No audio file path provided'}), 400

    audiofile =load_audio_from_url(request.form['audiofile'])
    
    try:
        # Transcribe the Hindi audio file
        transcription = asr_model_hi.transcribe([audiofile])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # Prepare the response JSON
    response_data = {
        'data_time': datetime.now().isoformat(),
        'transcribe': transcription[0]
    }

    return jsonify(response_data)

@app.route('/transcribe_en', methods=['POST'])
def transcribe_en():
    if 'audiofile_path' not in request.form:
        return jsonify({'error': 'No audio file path provided'}), 400

    audiofile_path = request.form['audiofile_path']
    
    try:
        # Transcribe the English audio file
        transcription = asr_model_en.transcribe([audiofile_path])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # Prepare the response JSON
    response_data = {
        'data_time': datetime.now().isoformat(),
        'transcribe': transcription[0]
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002) 
    
