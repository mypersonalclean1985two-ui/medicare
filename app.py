from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Medicare Bridge API")


class BridgeRequest(BaseModel):
    user_query: str | None = None


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "message": "Medicare Bridge API is running."
    }


@app.post("/bridge")
async def bridge(request: BridgeRequest):
    """
    This endpoint does NOT try to be smart.
    It just:
    - receives the user's text from ElevenLabs
    - (later) will call a real Medicare database
    - returns structured JSON for the LLM to use
    """
    user_text = (request.user_query or "").strip()

    # 🔜 LATER: replace this with a real database query.
    fake_db_result = {
        "db_status": "not_connected_yet",
        "notes": "This is a placeholder until we plug in a real Medicare database.",
        "plans": []
    }

    return {
        "content": "BRIDGE_OK",      # simple flag so we know the tool worked
        "raw_user_query": user_text, # what the caller actually said
        "data": fake_db_result       # where real DB data will live
    }
