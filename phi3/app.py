from flask import Flask, request, jsonify
from lmdeploy import pipeline,TurbomindEngineConfig

# decrease the ratio of the k/v cache occupation to 20%
backend_config = TurbomindEngineConfig(cache_max_entry_count=0.2)

app = Flask(__name__)

# Initialize the pipeline with the 'phi 3' model
pipe = pipeline('microsoft/Phi-3.5-mini-instruct',backend_config=backend_config)

@app.route('/generate', methods=['POST'])
def generate():
    # Get the input text from the POST request
    data = request.get_json()
    if not data or 'input_text' not in data:
        return jsonify({'error': 'No input_text provided'}), 400

    input_text = data['input_text']

    # Construct the prompt with the specified format
    prompt = f"<|system|>you are a call center operator. And you will give reply in json with the following parameters intent, language, appropriate answer and next step \n<|user|>\n{input_text}<|end|>\n<|assistant|>\n"

    # Get the response from the model
    response = pipe([prompt])
    print(response)

    # Return the response as JSON
    return jsonify({'response': response[0]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 
