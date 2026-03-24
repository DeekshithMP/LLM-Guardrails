from transformers import pipeline
from guardrails import detect_prompt_injection, detect_harmful

# Load lightweight toxicity model (CPU friendly)
classifier = pipeline("text-classification", model="unitary/toxic-bert")


def classify_prompt(text):
    text_lower = text.lower()

    # -------- RULE-BASED DETECTION -------- #

    # 1. Prompt Injection
    inj, _ = detect_prompt_injection(text)
    if inj:
        return {
            "category": "injection",
            "confidence": 0.85
        }

    # 2. Harmful keywords
    harm, _ = detect_harmful(text)
    if harm:
        return {
            "category": "harmful",
            "confidence": 0.75
        }

    # 3. Self-harm detection (robust)
    self_harm_patterns = [
        "hurt myself",
        "hurting myself",
        "kill myself",
        "suicide",
        "end my life",
        "want to die",
        "i want to hurt myself",
        "i want to die",
        "harm myself"
    ]

    if any(p in text_lower for p in self_harm_patterns):
        return {
            "category": "toxic",
            "confidence": 0.9
        }

    # 4. Hate speech detection
    if "hate" in text_lower:
        return {
            "category": "toxic",
            "confidence": 0.8
        }

    # -------- ML MODEL (TOXIC CLASSIFICATION) -------- #

    result = classifier(text)[0]
    label = result["label"]
    score = result["score"]

    # Scale confidence for threshold experiments
    confidence = float(score) * 0.7

    if "toxic" in label.lower():
        return {
            "category": "toxic",
            "confidence": confidence
        }

    # -------- DEFAULT SAFE -------- #

    return {
        "category": "safe",
        "confidence": confidence
    }