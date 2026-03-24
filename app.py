print("HELLO THIS IS NEW CODE")
from fastapi import FastAPI
from pydantic import BaseModel
import os
from groq import Groq
from dotenv import load_dotenv

from guardrails import (
    detect_prompt_injection,
    detect_harmful,
    restrict_domain,
    output_filter
)
from logger import log_event
from classifier import classify_prompt

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# Request schema
class Request(BaseModel):
    query: str


@app.post("/ask")
def ask_llm(req: Request):
    user_input = req.query

    # -------- CLASSIFIER -------- #
    result = classify_prompt(user_input)
    category = result["category"]
    confidence = result["confidence"]

    print("🔥 CLASSIFIER OUTPUT:", category, confidence)

    # 🚨 HARD BLOCK (NO EXCEPTIONS)
    if category != "safe":
        response = f"Blocked: {category} detected (confidence: {confidence:.2f})"
        log_event(user_input, response, "blocked")

        return {
            "response": response,
            "category": category,
            "confidence": confidence,
            "source": "guardrail"
        }

    # -------- RULE FALLBACK (extra safety) -------- #
    inj, pattern = detect_prompt_injection(user_input)
    if inj:
        response = f"Blocked: injection ({pattern})"
        log_event(user_input, response, "blocked")
        return {"response": response}

    harm, keyword = detect_harmful(user_input)
    if harm:
        response = f"Blocked: harmful ({keyword})"
        log_event(user_input, response, "blocked")
        return {"response": response}

    rest, topic = restrict_domain(user_input)
    if rest:
        response = f"Restricted: {topic}"
        log_event(user_input, response, "restricted")
        return {"response": response}

    # -------- LLM CALL -------- #
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": user_input}
            ]
        )

        answer = completion.choices[0].message.content

    except Exception as e:
        return {"error": str(e)}

    # -------- OUTPUT FILTER -------- #
    safe_output = output_filter(answer)

    log_event(user_input, safe_output, "success")

    return {
        "response": safe_output,
        "category": "safe",
        "confidence": confidence,
        "source": "llm"
    }