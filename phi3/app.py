from fastapi import FastAPI
from pydantic import BaseModel
from vllm import Phi3Model

app = FastAPI()

# Initialize the phi3 model (using vllm)
model = Phi3Model()

class GenerateTextRequest(BaseModel):
    prompt: str
    max_tokens: int = 50

class GenerateTextResponse(BaseModel):
    generated_text: str

@app.post("/generate-text", response_model=GenerateTextResponse)
async def generate_text(request: GenerateTextRequest):
    # Generate text using the phi3 model from vllm
    generated = model.generate(prompt=request.prompt, max_tokens=request.max_tokens)
    
    return GenerateTextResponse(generated_text=generated)
