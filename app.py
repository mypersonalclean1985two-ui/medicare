from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any

# For now we are NOT connecting to medicare.db yet.
# First we just prove that ElevenLabs -> Render -> FastAPI -> back works.

app = FastAPI(title="Medicare Bridge API")

class BridgeRequest(BaseModel):
    user_query: str | None = None

@app.get("/health")
def health() -> Dict[str, Any]:
    """
    Simple health check endpoint.
    """
    return {"status": "ok", "message": "Medicare Bridge API on Render is running."}

@app.post("/bridge")
def bridge(req: BridgeRequest) -> Dict[str, Any]:
    """
    Main endpoint that ElevenLabs will call as a tool.
    For now it just echoes back what it received.
    Later we can add real medicare.db lookups here.
    """
    text = req.user_query or ""
    reply = f"Render Medicare bridge received this query from ElevenLabs: {text}"
    return {
        "content": reply,
        "raw_user_query": text,
    }
