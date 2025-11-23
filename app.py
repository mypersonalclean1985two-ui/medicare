from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Medicare Bridge API v2")


class BridgeRequest(BaseModel):
    user_query: str | None = None


@app.get("/health")
async def health_check():
    # NOTICE: message is different now (v2)
    return {
        "status": "ok",
        "message": "Medicare Bridge API v2 is running."
    }


@app.post("/bridge")
async def bridge(request: BridgeRequest):
    user_text = (request.user_query or "").strip()

    # SUPER SIMPLE TEST RESPONSE
    content = (
        "THIS IS VERSION 2 OF THE MEDICARE BRIDGE. "
        "You said: " + (user_text or "[no text received].")
    )

    return {
        "content": content,
        "raw_user_query": user_text,
    }
