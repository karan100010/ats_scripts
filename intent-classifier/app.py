from flask import Flask, request, jsonify
from transformers import pipeline

pipe = pipeline("text-classification",
                model="vineetsharma/customer-support-intent-albert")


app = Flask(__name__)


@app.route('/predict_intent', methods=['POST'])
def predict():
    text = request.json['text']
    result = pipe(text)
    return jsonify(result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5007)
