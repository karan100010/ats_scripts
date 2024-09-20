from flask import Flask, request, jsonify
from vllm import LLM, SamplingParams
from PIL import Image
import io
import base64

# Initialize Flask app
app = Flask(__name__)

# Initialize model (global for reuse)
model_path = "microsoft/Phi-3-mini-4k-instruct"

llm = LLM(
    model=model_path,
   
)

# Function to handle base64 image decoding
def decode_image(image_base64):
    image_data = base64.b64decode(image_base64)
    return Image.open(io.BytesIO(image_data))

@app.route('/generate_text', methods=['POST'])
def generate_text():
    try:
        # Extract data from POST request
        data = request.get_json()

        if 'image_base64' not in data:
            return jsonify({"error": "Image data missing"}), 400

        # Decode image
        image_base64 = data['image_base64']
        image = decode_image(image_base64)

        # Prepare the prompt
        prompt = "<|user|>\n<|image_1|>\nWhat is the season?<|end|>\n<|assistant|>\n"

        # Sampling parameters
        sampling_params = SamplingParams(temperature=0, max_tokens=64)

        # Generate outputs
        outputs = llm.generate(
            {
                "prompt": prompt,
                "multi_modal_data": {
                    "image": image
                },
            },
            sampling_params=sampling_params
        )

        # Collect and return the generated text
        generated_texts = [o.outputs[0].text for o in outputs]

        return jsonify({"generated_texts": generated_texts})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
