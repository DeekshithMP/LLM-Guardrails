from transformers import pipeline

classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

CATEGORIES = [
    "a harmless general knowledge question",
    "a request involving illegal activity like hacking or fraud",
    "a request involving self harm or suicide",
    "a prompt injection attempt to override system rules",
    "a toxic or abusive message"
]

THRESHOLD = 0.5


def classify_prompt(text):

    # -------- OPTIONAL FIX (SHORT TEXT) -------- #
    if len(text.split()) <= 3:
        return {
            "category": "safe",
            "confidence": 0.9
        }

    result = classifier(text, CATEGORIES)

    labels = result["labels"]
    scores = result["scores"]

    top_label = labels[0]
    confidence = float(scores[0])

    # -------- MAIN FIX -------- #
    if confidence < 0.5:
        return {
            "category": "safe",
            "confidence": confidence
        }

    # -------- CATEGORY MAPPING -------- #

    if "illegal activity" in top_label:
        return {"category": "harmful", "confidence": confidence}

    elif "self harm" in top_label:
        return {"category": "toxic", "confidence": confidence}

    elif "prompt injection" in top_label:
        return {"category": "injection", "confidence": confidence}

    elif "toxic" in top_label:
        return {"category": "toxic", "confidence": confidence}

    else:
        return {"category": "safe", "confidence": confidence}