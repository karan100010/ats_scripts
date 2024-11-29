import dspy
from flask import Flask, request, jsonify

lm = dspy.LM("openai/microsoft/Phi-3.5-mini-instruct",
             api_base="http://localhost:23333/v1",  # ensure this points to your port
             api_key="local", model_type='chat')

dspy.configure(lm=lm)
lm("Say this is a test!", temperature=0.7)  # => ['This is a test!']
lm(messages=[{"role": "user", "content": "Say this is a test!"}])  # => ['This is a test!']



# Assuming dspy and ExtractInfo are defined as per your example
class ExtractInfo(dspy.Signature):
    """Extract structured information from text."""
    text: str = dspy.InputField()
    title: str = dspy.OutputField()
    headings: list[str] = dspy.OutputField()
    entities: list[dict[str, str]] = dspy.OutputField(desc="a list of entities and their metadata")

# Initialize the module
module = dspy.Predict(ExtractInfo)

app = Flask(__name__)

@app.route('/extract', methods=['POST'])
def extract_entities():
    # Get the input text from the POST request
    data = request.get_json()
    text = data.get('text', '')
    print(text)

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    # Use the module to extract entities
    response = module(text=text)
    # Assuming entities are returned in the response as a list of dictionaries
    entities = response.entities  # Access the 'entities' output field

    sentences = []
    for entity in entities:
        name = entity.get('name')
        type_ = entity.get('type')  # Using 'type_' to avoid conflict with built-in 'type'

        if name and type_:
            sentence = f"{name} is a {type_}"
            sentences.append(sentence)

    return jsonify({'sentences': sentences})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5014) 


