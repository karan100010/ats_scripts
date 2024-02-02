import torch
from transformers import AlbertForSequenceClassification, AlbertTokenizer
from datasets import ClassLabel

# Load the saved model
model_path = "./model"
model = AlbertForSequenceClassification.from_pretrained(model_path)

# Load the tokenizer
tokenizer = AlbertTokenizer.from_pretrained("albert-base-v2")

# Input text for testing
input_text = "This is not her"

# Tokenize and convert to tensor
inputs = tokenizer(input_text, return_tensors="pt")

# Make inference
with torch.no_grad():
    outputs = model(**inputs)

# Get the predicted class
logits = outputs.logits
predicted_class = torch.argmax(logits, dim=1).item()

print(f"Predicted Class: {predicted_class}")

c2l = ClassLabel(num_classes=28, names=['change_shipping_address', 'track_order', 'edit_account', 'payment_issue', 'switch_account', 'contact_human_agent', 'place_order', 'delivery_options', 'newsletter_subscription', 'check_payment_methods', 'contact_customer_service', 'get_refund',
                 'delivery_period', 'delete_account', 'create_account', 'check_invoice', 'track_refund', 'complaint', 'registration_problems', 'get_invoice', 'cancel_order', 'wrong_number', 'review', 'check_cancellation_fee', 'recover_password', 'check_refund_policy', 'set_up_shipping_address', 'change_order'])

print(c2l.int2str(predicted_class))
