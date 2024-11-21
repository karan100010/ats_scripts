import os
from dspy import Pipeline
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
from sentence_transformers import SentenceTransformer
import numpy as np

# Initialize Qdrant client
qdrant_client = QdrantClient(host='localhost', port=6333)

# Name of the collection in Qdrant
collection_name = 'emi_recovery_prompts'

# Load the embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Determine the vector size from the model
vector_size = embedding_model.get_sentence_embedding_dimension()

# Ensure the collection exists
qdrant_client.recreate_collection(
    collection_name=collection_name,
    vector_size=vector_size,  # Embedding size from the model
    distance='Cosine'
)

# Your prompt
prompt = """<|system|>
You are an expert in designing call flow systems for financial services, specifically focused on EMI (Equated Monthly Installment) recovery.

**Objective:**
Help me create a call flow script that efficiently handles incoming calls related to EMI recovery, integrating the caller's inputs directly into the flow to guide them through settling overdue payments.

**Requirements:**

1. **Greeting:**
   - Start with a professional and empathetic greeting.
     - Example: "Thank you for calling XYZ Financial Services. How may we assist you today?"

2. **Identification and Verification:**
   - Prompt the caller to provide necessary identification details to verify their account.
     - Example: "To assist you better, may I have your account number and date of birth?"

3. **Integration of Caller’s Input:**
   - Use the caller's responses to personalize the conversation and guide the call flow.
     - Examples:
       - If the caller mentions difficulty in making payments, offer alternative payment plans.
       - If the caller wants to make an immediate payment, guide them through the payment process.

4. **EMI Recovery Process:**
   - Provide information about overdue payments based on the verified account details.
   - Use the caller's input to determine the best course of action.
     - If the caller agrees to pay:
       - Confirm the amount and due date.
       - Offer various payment methods (online, phone, etc.).
     - If the caller requests an extension:
       - Check eligibility and provide options.
       - Document the agreed-upon arrangement.

5. **Handling Objections and Concerns:**
   - Address any concerns or objections the caller may have, using their specific inputs.
     - Example:
       - "I understand that you're facing difficulties due to [caller’s reason]. Let's see how we can assist you."

6. **Compliance and Legal Considerations:**
   - Ensure all communications comply with relevant financial regulations and privacy laws.
   - Use appropriate language that is respectful and non-threatening.

7. **Recording and Utilizing Caller Input:**
   - Record the caller's responses for future reference and compliance.
   - Use the input to update the customer's account status in real-time.

8. **Closing:**
   - Summarize the agreed-upon actions using the caller's input.
     - Example: "To confirm, you will make a payment of [amount] by [date] via [payment method]. Is that correct?"
   - End the call with a polite and professional closing.
     - Example: "Thank you for your time, [caller’s name]. If you have any further questions, please don't hesitate to call us again."

**Deliverable:**
Provide a detailed call flow script or pseudo-code that I can use to implement this EMI recovery system in our customer service operations, ensuring that the caller's inputs are seamlessly integrated into each step of the flow.

**Technical Considerations:**
- Assume the system may use speech recognition to handle voice inputs.
- Design the system to dynamically respond to the caller's input at each stage.
- Include data handling practices to securely process and store sensitive information.
- Ensure quick response times and a user-friendly experience.

**Suggestions for Improvement:**
- Recommend strategies to personalize the call flow based on the caller's input.
- Suggest methods to improve compliance and data security when handling user input.
- Provide guidance on handling edge cases where caller input may be unclear or incomplete.
<|end|>
<|user|>
<|end|>
<|assistant|>"""

# Generate embedding for the prompt
prompt_embedding = embedding_model.encode(prompt)

# Ensure the embedding is a list (Qdrant expects list, not numpy array)
prompt_embedding = prompt_embedding.tolist()

# Insert the prompt into Qdrant
qdrant_client.upsert(
    collection_name=collection_name,
    points=[
        PointStruct(
            id=1,
            vector=prompt_embedding,
            payload={"text": prompt}
        )
    ]
)

# Define the DSPy pipeline
pipeline = Pipeline()

# Add a step to retrieve similar prompts from Qdrant based on user input
def retrieve_similar_prompts(user_input):
    user_embedding = embedding_model.encode(user_input).tolist()
    search_result = qdrant_client.search(
        collection_name=collection_name,
        query_vector=user_embedding,
        limit=1
    )
    if search_result:
        return search_result[0].payload['text']
    else:
        return "No relevant prompts found."

pipeline.add_step('RetrievePrompt', retrieve_similar_prompts)

# Add a step to generate a response using an open-source language model
def generate_response(retrieved_prompt):
    # Use a local LLM via Hugging Face Transformers
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch

    # Load the model and tokenizer (you may choose a different model)
    model_name = 'gpt2-medium'  # Replace with a larger model if needed
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    # Prepare the input
    input_ids = tokenizer.encode(retrieved_prompt + "\n", return_tensors='pt')

    # Generate the response
    output_ids = model.generate(
        input_ids,
        max_length=1024,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        num_return_sequences=1
    )

    # Decode the output
    response_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    # Extract the assistant's response
    assistant_response = response_text[len(retrieved_prompt):].strip()
    return assistant_response

pipeline.add_step('GenerateResponse', generate_response)

# Execute the pipeline with user input
if __name__ == "__main__":
    user_input = input("Enter your query: ")
    retrieved_prompt = pipeline.run_step('RetrievePrompt', user_input)
    assistant_response = pipeline.run_step('GenerateResponse', retrieved_prompt)
    print("\nAssistant's Response:\n")
    print(assistant_response)
