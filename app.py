from fastapi import FastAPI
from pydantic import BaseModel
import os
from groq import Groq

from guardrails import (
    detect_prompt_injection,
    detect_harmful,
    restrict_domain,
    output_filter
)
from logger import log_event

app = FastAPI()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class Request(BaseModel):
    query: str


@app.post("/ask")
def ask_llm(req: Request):
    user_input = req.query

    # -------- INPUT GUARDRAILS -------- #

    inj, pattern = detect_prompt_injection(user_input)
    if inj:
        response = f"Blocked: Prompt injection detected (pattern: {pattern})"
        log_event(user_input, response, "blocked")
        return {"response": response}

    harm, keyword = detect_harmful(user_input)
    if harm:
        response = f"Blocked: Harmful query detected (keyword: {keyword})"
        log_event(user_input, response, "blocked")
        return {"response": response}

    rest, topic = restrict_domain(user_input)
    if rest:
        response = f"Restricted: Cannot provide advice on {topic}"
        log_event(user_input, response, "restricted")
        return {"response": response}

    # -------- LLM CALL -------- #

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful and safe AI assistant."},
                {"role": "user", "content": user_input}
            ]
        )

        answer = completion.choices[0].message.content

    except Exception as e:
        return {"error": str(e)}

    # -------- OUTPUT GUARDRAILS -------- #

    safe_output = output_filter(answer)

    log_event(user_input, safe_output, "success")

    return {"response": safe_output}