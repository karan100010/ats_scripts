import spacy
from functions import get_entities, get_sentiment
from flask import Flask, request, jsonify

from spacytextblob.spacytextblob import SpacyTextBlob
from transformers import AlbertForSequenceClassification, AlbertTokenizer
from datasets import ClassLabel
import torch


nlp = spacy.load("en_core_web_trf", disable=[
                 "tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"])
nlp.add_pipe('spacytextblob')


# Load the saved model
model_path = "./model"
model = AlbertForSequenceClassification.from_pretrained(model_path)

# Load the tokenizer
tokenizer = AlbertTokenizer.from_pretrained("albert-base-v2")
label_classes = ["yes_intent", "no_intent", "call_back_later_intent", "contact_human_agent_intent", "other_intent"]
# Intent Labels
c2l = ClassLabel(num_classes=len(label_classes), names=label_classes)

    
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

    # Tokenize and convert to tensor
    inputs = tokenizer(text, return_tensors="pt")

    # Make inference
    with torch.no_grad():
        outputs = model(**inputs)

    # Get the predicted class
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()
    confidence = torch.max(logits).item()
    import torch
    import torch.nn.functional as F

    def softmax(logits):
        return F.softmax(logits, dim=1)

    softmaxed_logits = softmax(logits)
    print(f"Normalized Logits: ", {softmaxed_logits})
    print(torch.argmax(softmaxed_logits, dim=1).item())



    THRESHOLD = 3.6
    if predicted_class == 2:
        THRESHOLD = 2

    if confidence < THRESHOLD:
        print("other_intent")
        intent="other_intent"
    else:
        print(c2l.int2str(predicted_class))
        intent = c2l.int2str(predicted_class)

    return jsonify({"entities": entities,
                    "sentiment": sentiment,
                    "intent": intent
                    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
