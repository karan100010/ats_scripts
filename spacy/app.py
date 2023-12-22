import spacy
from functions import get_entities, get_sentiment
from flask import Flask, request, jsonify

from spacytextblob.spacytextblob import SpacyTextBlob


nlp = spacy.load("en_core_web_trf", disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"])
nlp.add_pipe('spacytextblob')

app = Flask(__name__)

@app.route('/api_status', methods=['GET'])
def api_status():
    return jsonify({
        "status": "ok", 
        "message": "spacy is up and running"
        }), 200


@app.route('/get_entities', methods=['POST'])
def entities():
    try:
        text = request.json['sentence']
    except:
        return jsonify({"error": "no sentence found"}), 400
    
    entities = get_entities(text, nlp)
    sentiment = get_sentiment(text, nlp)
    return jsonify({"entities":entities,
                    "sentiment":sentiment  }), 200




if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001)