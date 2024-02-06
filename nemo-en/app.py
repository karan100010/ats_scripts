from flask import Flask, request, jsonify
from datetime import datetime
import nemo.collections.asr as nemo_asr
import requests
import tempfile
import os
import json
import wave
import json
import nemo.collections.nlp as nemo_nlp
app = Flask(__name__)


def convert_file(file):
    # Decode and combine u-law fragments into a single bytearray
    # Remove the unused line of code
    # combined_pcm_data = bytearray()

    # ulaw_data = bytes(file['data']['data'])

    # Decode the u-law data to 16-bit linear PCM
    # pcm_data = audioop.ulaw2lin(file, 2)

    # Save the combined PCM data to a WAV file
    with wave.open('output.wav', 'wb') as wf:
        wf.setnchannels(1)  # Adjust based on the number of channels in your audio
        wf.setsampwidth(2)  # 2 bytes for 16-bit audio
        wf.setframerate(8000)  # Adjust based on the sample rate of your u-law audio
        wf.writeframes(file)
asr_model_hi = nemo_asr.models.EncDecCTCModelBPE.from_pretrained(model_name="stt_hi_conformer_ctc_medium")

nmt_model = nemo_nlp.models.machine_translation.MTEncDecModel.from_pretrained(model_name="nmt_hi_en_transformer12x2")

@app.route('/api_status', methods=['GET'])
def api_status():
    return jsonify({
        "status": "ok",
        "message": "nemo is up and running"
        }), 200


# Load the English ASR model
asr_model_en = nemo_asr.models.EncDecCTCModelBPE.from_pretrained(model_name="stt_en_conformer_ctc_medium")
def load_audio_from_url(url):
    # Make a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Create a temporary directory to store the audio file
        temp_dir = tempfile.mkdtemp()
        local_file_path = os.path.join(temp_dir, "temp_audio.mp3")

        # Write the audio content to the temporary file
        with open(local_file_path, "wb") as temp_file:
            temp_file.write(response.content)

        return local_file_path
    else:
        print(f"Failed to fetch audio from {url}. Status code: {response.status_code}")
        return None
    



@app.route('/transcribe_hi', methods=['POST'])
def transcribe_hi():
    if 'audiofile' not in request.form:
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

    return json.dumps(response_data,ensure_ascii=False)

@app.route('/transcribe_en', methods=['POST'])
def transcribe_en():
    if 'audiofile' not in request.form:
        return jsonify({'error': 'No audio file path provided'}), 400
    
    audiofile =load_audio_from_url(request.form['audiofile'])
    
    try:
        # Transcribe the English audio file
        transcription = asr_model_en.transcribe([audiofile])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # Prepare the response JSON
    response_data = {
        'data_time': datetime.now().isoformat(),
        'transcribe': transcription[0]
    }

    return jsonify(response_data)

@app.route('/convert_en', methods=['POST'])
def convert_ulaw_to_wave():

    print(request.get_data())
    ulaw_fragments  = request.get_data()
    print(ulaw_fragments)
    #convert ulaw_fragment variable to a array

    print(type(ulaw_fragments))
    #writ ulaw_fragments to a json file
    convert_file(ulaw_fragments)
    text=asr_model_en.transcribe(["output.wav"])
    #delete the file output.wav
    os.remove("output.wav")
    response_data = {
        'data_time': datetime.now().isoformat(),
        'transcribe': text[0]
    }

    return jsonify(response_data)

@app.route('/convert_en', methods=['POST'])
def convert_ulaw_to_wave_hi():

    print(request.get_data())
    ulaw_fragments  = request.get_data()
    print(ulaw_fragments)
    #convert ulaw_fragment variable to a array

    print(type(ulaw_fragments))
    #writ ulaw_fragments to a json file
    convert_file(ulaw_fragments)
    text=asr_model_hi.transcribe(["output.wav"])
    #delete the file output.wav
    result = nmt_model.translate([text[0]], source_lang="hi", target_lang="en")
    os.remove("output.wav")
    response_data = {
        'data_time': datetime.now().isoformat(),
        'transcribe': result[0]
    }

    return jsonify(response_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002) 

