from flask import Flask, request, jsonify
import lmdeploy
from lmdeploy import LM
import torch

# Initialize Flask app
app = Flask(__name__)

# Model path and quantization configurations
model_path = "microsoft/Phi-3-mini-4k-instruct"

# Initialize model with lmdeploy
model = LM(
    model_path=model_path,
    use_quantization=True,  # Enable quantization, if needed
    quantization_method="awq",  # Quantization method
    dtype="fp16",  # Data type
    gpu_memory_utilization=0.5  # GPU memory utilization
)

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
        
        # Generate outputs using the model
        generated_output = model.generate(prompt, temperature=0, max_tokens=64)
        
        # Collect and return the generated text
        generated_text = generated_output[0]
        return jsonify({"generated_texts": [generated_text]})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

