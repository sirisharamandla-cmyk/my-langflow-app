from fastapi import FastAPI, Header
from pydantic import BaseModel
import requests
import os

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
def run_langflow(request: ChatRequest):
    # Retrieve secrets from Vercel Environment Variables
    flow_id = os.environ.get("LANGFLOW_FLOW_ID")
    api_key = os.environ.get("LANGFLOW_API_KEY")
    base_url = os.environ.get("LANGFLOW_BASE_URL", "https://api.langflow.astra.datastax.com")

    # API call to Langflow's processing engine
    url = f"{base_url}/api/v1/run/{flow_id}"
    headers = {"Content-Type": "application/json", "x-api-key": api_key}
    payload = {
        "input_value": request.message,
        "output_type": "chat",
        "input_type": "chat"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()
