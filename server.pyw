import time
from typing import List
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.security import APIKeyHeader
from pydantic import BaseModel

app = FastAPI(title="Production-Ready AI Server")

# 1. CORS Setup (Allows frontends like React, Vue, or Next.js to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Simple API Key Security
API_KEY = "my-secret-ai-token"
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

def verify_api_key(key: str = Security(api_key_header)):
    if key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return key

# 3. Request Data Structures
class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    stream: bool = False

# Mock streaming generator
def dummy_stream_generator(prompt: str):
    response_text = f"Streaming response for: '{prompt}' token by token."
    for word in response_text.split():
        yield f"data: {word} \n\n"
        time.sleep(0.2)  # Simulates model generation delay
    yield "data: [DONE]\n\n"

@app.get("/")
def health_check():
    return {"status": "healthy", "timestamp": time.time()}

# 4. Secure Chat Endpoint with Streaming option
@app.post("/v1/chat/completions")
def chat_completion(data: ChatRequest, api_key: str = Depends(verify_api_key)):
    if not data.messages:
        raise HTTPException(status_code=400, detail="Messages list cannot be empty")
    
    # Grab the latest user prompt
    last_user_prompt = data.messages[-1].content
    
    # Handle Streaming Response
    if data.stream:
        return StreamingResponse(dummy_stream_generator(last_user_prompt), media_type="text/event-stream")
    
    # Handle Standard JSON Response
    return {
        "choices": [{
            "message": {
                "role": "assistant",
                "content": f"Standard response to: '{last_user_prompt}'. This endpoint is conversation-aware."
            }
        }]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
