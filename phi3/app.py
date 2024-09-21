from flask import Flask, request, jsonify
from vllm import LLM, SamplingParams

# Initialize Flask app
app = Flask(__name__)

# Initialize model (global for reuse)
model_path = "microsoft/Phi-3-mini-4k-instruct"
llm = LLM(model=model_path)

@app.route('/generate_text', methods=['POST'])
def generate_text():
    try:
        # Extract data from POST request
        data = request.get_json()
        if 'prompt' not in data:
            return jsonify({"error": "Input text missing"}), 400
        
        # Get the input text
        input_text = data['prompt']
        
        # Prepare the prompt
        prompt = f"<|system|>you are a call center operator. And you will give reply in json with the following parameters intent, language, appropriate answer and next step \n<|user|>\n{input_text}<|end|>\n<|assistant|>\n"
        
        # Sampling parameters
        sampling_params = SamplingParams(temperature=0, max_tokens=64)
        
        # Generate outputs
        outputs = llm.generate(prompt, sampling_params=sampling_params)
        
        # Collect and return the generated text
        generated_texts = [o.outputs[0].text for o in outputs]
        return jsonify({"generated_texts": generated_texts})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

