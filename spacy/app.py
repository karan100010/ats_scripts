import spacy
from functions import get_entities
from flask import Flask, request, jsonify

nlp = spacy.load("en_core_web_trf", disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"])

app = Flask(__name__)

@app.route('/api_status', methods=['GET'])
def api_status():
    return jsonify({
        "status": "ok", 
        "message": "spacy is up and running"
        }), 200


@app.route('/get_entities', methods=['POST'])
def entities():
    data = request.json
    text = data['sentence']
    entities = get_entities(text[0], nlp)
    return jsonify(entities)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001)