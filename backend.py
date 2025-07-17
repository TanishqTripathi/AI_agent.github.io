from pydantic import BaseModel
from typing import List

class RequestState(BaseModel):
    model_name: str
    model_provider: str
    # system_prompt: str
    messages: List[str]
    allow_search: bool
    system_prompt: str

from fastapi import FastAPI
from Agentic_ai import get_response_from_ai

ALLOWED_MODELS = ["llama-3.3-70b-versatile"]

app = FastAPI(title="Agentic AI API",)

@app.post("/chat")
def chat_endpoint(request_state: RequestState):
    """
    Endpoint to handle chat requests.
    """
    if request_state.model_name not in ALLOWED_MODELS:
        return {"error": "Model not allowed."}
    
    llm_id = request_state.model_name
    query = request_state.messages
    # system_prompt = request_state.system_prompt
    allow_search = request_state.allow_search
    model_provider = request_state.model_provider
    system_prompt = request_state.system_prompt
    
    response = get_response_from_ai(llm_id, query, allow_search, model_provider,system_prompt)
    return response
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)