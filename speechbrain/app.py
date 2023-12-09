from flask import Flask, request, jsonify
import torchaudio
from speechbrain.pretrained import EncoderClassifier

app = Flask(__name__)

# Load the language identification model
language_id = EncoderClassifier.from_hparams(source="speechbrain/lang-id-voxlingua107-ecapa", savedir="tmp")

@app.route('/api_status', methods=['GET'])
def api_status():
    return jsonify({
        "status": "ok", 
        "message":"speechbrain is up and running"
        }), 200

@app.route('/predict_language', methods=['POST'])
def predict_language():
    try:
        filepath = request.json['filepath']
        
        
        # Load the audio file
        signal = language_id.load_audio(filepath)


        # Perform language identification
        prediction = language_id.classify_batch(signal)

        # Prepare response
        response = {
            "predicted_language": prediction[3][0],  # Get the first language in case of multiple predictions
            "confidence": float(prediction[1].exp())
        }

        return jsonify(response), 200

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
    
#new code from below this line

import wave
import audioop
import json

def convert_file(file):
    # Decode and combine u-law fragments into a single bytearray
    combined_pcm_data = bytearray()
    ulaw_data = bytes(file['data']['data'])


    # Decode the u-law data to 16-bit linear PCM
    pcm_data = audioop.ulaw2lin(ulaw_data, 2)


    # Save the combined PCM data to a WAV file
    with wave.open('outputx.wav', 'wb') as wf:
        wf.setnchannels(1)  # Adjust based on the number of channels in your audio
        wf.setsampwidth(2)  # 2 bytes for 16-bit audio
        wf.setframerate(8000)  # Adjust based on the sample rate of your u-law audio
        wf.writeframes(pcm_data)
@app.route('/convert', methods=['POST'])
def convert_ulaw_to_wave():


# Assuming you have an array of u-law encoded fragments
    ulaw_fragments = request.get_json()
    print(ulaw_fragments)
    #convert ulaw_fragment variable to a array

    print(type(ulaw_fragments))
    #writ ulaw_fragments to a json file
    convert_file(ulaw_fragments)
        # Perform language identification
    prediction = language_id.classify_batch("outputx.wav")

    # Prepare response
    response = {
        "predicted_language": prediction[3][0],  # Get the first language in case of multiple predictions
        "confidence": float(prediction[1].exp())
    }


    return jsonify(response)
        


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


