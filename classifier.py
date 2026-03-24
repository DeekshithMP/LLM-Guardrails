from transformers import pipeline

classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

CATEGORIES = [
    "safe",
    "toxic",
    "self-harm",
    "prompt injection",
    "harmful instruction"
]


def classify_prompt(text):
    text_lower = text.lower()

    # -------- STRONG SAFETY OVERRIDES -------- #

    # Self-harm
    if any(word in text_lower for word in ["hurt", "kill", "suicide", "die", "harm"]):
        return {"category": "toxic", "confidence": 0.95}

    # Hacking / illegal
    if "hack" in text_lower:
        return {"category": "harmful", "confidence": 0.95}

    # Dangerous actions
    if any(word in text_lower for word in ["bomb", "attack", "weapon"]):
        return {"category": "harmful", "confidence": 0.9}

    # Injection
    if "ignore previous instructions" in text_lower:
        return {"category": "injection", "confidence": 0.9}

    # -------- ML CLASSIFICATION -------- #

    result = classifier(text, CATEGORIES)

    top_label = result["labels"][0]
    confidence = float(result["scores"][0])

    if top_label == "self-harm":
        return {"category": "toxic", "confidence": confidence}

    elif top_label == "toxic":
        return {"category": "toxic", "confidence": confidence}

    elif top_label == "prompt injection":
        return {"category": "injection", "confidence": confidence}

    elif top_label == "harmful instruction":
        return {"category": "harmful", "confidence": confidence}

    else:
        return {"category": "safe", "confidence": confidence}