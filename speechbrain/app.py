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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
