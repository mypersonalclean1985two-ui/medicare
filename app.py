from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Medicare Bridge API")


class BridgeRequest(BaseModel):
    user_query: str | None = None


@app.get("/health")
async def health_check():
    """
    Simple health check so Render (and you) can see if the app is alive.
    """
    return {
        "status": "ok",
        "message": "Medicare Bridge API on Render is running."
    }


@app.post("/bridge")
async def bridge(request: BridgeRequest):
    """
    Main endpoint that ElevenLabs calls.

    It receives JSON like:
      { "user_query": "user's question" }

    and returns:
      {
        "content": "What the agent should say out loud",
        "raw_user_query": "original text from the caller"
      }
    """
    user_text = (request.user_query or "").strip()
    print(f"[bridge] user_query = {user_text!r}")  # shows up in Render logs

    # If nothing was sent, ask the caller to repeat.
    if not user_text:
        content = (
            "Thanks for calling about Medicare. "
            "I didn't quite catch your question. "
            "Could you please tell me your age, whether you're still working, "
            "and if you already have any Medicare or employer coverage?"
        )
        return {"content": content, "raw_user_query": user_text}

    # Start with a friendly, generic answer
    content = (
        "Thank you for sharing that. Right now I'm a demo Medicare assistant, "
        "so I can't see your personal records yet, "
        "but here’s some general guidance for someone in your situation.\n\n"
    )

    text_lower = user_text.lower()

    # Very simple “rules” just to sound smarter than an echo.
    if "retire" in text_lower or "retired" in text_lower:
        content += (
            "Because you mentioned retirement, the key things to look at are: "
            "your age, when your employer coverage ends, and whether you already "
            "have Medicare Parts A and B. "
            "In many cases, people enroll in Part B when their employer coverage "
            "is ending, then compare Medicare Advantage and Medigap options in "
            "their area.\n"
        )
    elif "plan" in text_lower or "advantage" in text_lower or "supplement" in text_lower:
        content += (
            "When choosing a Medicare plan, the big items to compare are: "
            "which doctors are in network, which prescriptions are covered, "
            "the monthly premium, and the yearly maximum you might pay out of pocket.\n"
        )
    else:
        content += (
            "Here are the basics: Medicare Part A usually helps with hospital stays, "
            "Part B helps with doctor visits and outpatient care, "
            "Part D covers prescriptions, and you can choose either a Medicare "
            "Advantage plan or a Medigap supplement for extra protection.\n"
        )

    content += (
        "\nIn the full version of this assistant, I will connect to a secure Medicare "
        "database to look up real plans based on your ZIP code and needs, and then "
        "walk you through simple, clear choices. "
        "For now, this is general information, not a recommendation."
    )

    return {
        "content": content,
        "raw_user_query": user_text,
    }
