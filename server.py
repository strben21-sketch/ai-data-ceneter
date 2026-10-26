from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Simple AI Server")

class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    return {"status": "AI Server is running!"}

@app.post("/generate")
def generate_response(data: PromptRequest):
    if not data.prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    
    # Replace this mock logic with your actual AI model inference (e.g., Ollama, Llama.cpp, or OpenAI SDK)
    ai_reply = f"Echo from AI server: You said '{data.prompt}'"
    
    return {"response": ai_reply}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
