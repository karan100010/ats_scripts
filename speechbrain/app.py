from flask import Flask, request, jsonify
import os
from speechbrain.pretrained import EncoderClassifier
from speechbrain.pretrained import  EncoderClassifier, SpeakerRecognition
import wave
from datetime import datetime

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
        # Upsample the audio to 16000 sample rate
        
        wf.setnchannels(1)  # Adjust based on the number of channels in your audio
        wf.setsampwidth(2)  # 2 bytes for 16-bit audio
        wf.setframerate(8000)  # Adjust based on the sample rate of your u-law audio
        wf.writeframes(file)
    #os.system("x -r 16000 -e unsigned -b 8 -c 1 output.wav output.wav")  # Convert the audio to 16kHz sample rate

# Load the language identification model
model_path = "model/epaca/1988/save/CKPT+2024-02-15+14-26-50+00/"
print(os.path.exists(model_path))
model = SpeakerRecognition.from_hparams(source=model_path)

#language_id = EncoderClassifier.from_hparams(source="speechbrain/lang-id-voxlingua107-ecapa", savedir="tmp")

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
        # signal = language_id.load_audio(filepath)


        # Perform language identification
        prediction = model.classify_file(filepath)

        # Prepare response
        response = {
            "predicted_language": prediction[3],  # Get the first language in case of multiple predictions
            "confidence": float(prediction[1].exp())
        }

        return jsonify(response), 200

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
@app.route('/predict', methods=['POST'])
def convert_ulaw_to_wave():

    print(request.get_data())
    ulaw_fragments  = request.get_data()
    print(ulaw_fragments)
    #convert ulaw_fragment variable to a array

    print(type(ulaw_fragments))
    #writ ulaw_fragments to a json file
    convert_file(ulaw_fragments)
    prediction = model.classify_file("output.wav")
    #delete the file output.wav

    response_data = {
        'data_time': datetime.now().isoformat(),
        'prediction':prediction[3]
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
