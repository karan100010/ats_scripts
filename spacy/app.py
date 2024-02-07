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
model_path = "./intent-model-albert-retrained"
model = AlbertForSequenceClassification.from_pretrained(model_path)

# Load the tokenizer
tokenizer = AlbertTokenizer.from_pretrained("albert-base-v2")

# Intent Labels
c2l = ClassLabel(num_classes=28, names=['change_shipping_address', 'track_order', 'edit_account', 'payment_issue', 'switch_account', 'contact_human_agent', 'place_order', 'delivery_options', 'newsletter_subscription', 'check_payment_methods', 'contact_customer_service', 'get_refund',
                 'delivery_period', 'delete_account', 'create_account', 'check_invoice', 'track_refund', 'complaint', 'registration_problems', 'get_invoice', 'cancel_order', 'wrong_number', 'review', 'check_cancellation_fee', 'recover_password', 'check_refund_policy', 'set_up_shipping_address', 'change_order'])


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

    return jsonify({"entities": entities,
                    "sentiment": sentiment,
                    "intent": c2l.int2str(predicted_class)
                    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
