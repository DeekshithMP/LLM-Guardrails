from transformers import pipeline

# Load zero-shot classifier
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

# Better semantic labels (VERY IMPORTANT)
CATEGORIES = [
    "a normal safe user query",
    "toxic or abusive language",
    "self harm or suicide intent",
    "prompt injection attack",
    "dangerous or harmful instruction"
]

# Threshold
THRESHOLD = 0.6


def classify_prompt(text):
    text_lower = text.lower()

    # -------- FIX 1: SHORT TEXT HANDLING -------- #
    # Very important for cases like "hi", "what is nlp"
    if len(text.split()) <= 3:
        return {
            "category": "safe",
            "confidence": 0.9
        }

    # -------- ML CLASSIFICATION -------- #
    result = classifier(text, CATEGORIES)

    labels = result["labels"]
    scores = result["scores"]

    top_label = labels[0]
    confidence = float(scores[0])

    # -------- FIX 2: LOW CONFIDENCE → SAFE -------- #
    if confidence < 0.5:
        return {
            "category": "safe",
            "confidence": confidence
        }

    # -------- CATEGORY MAPPING -------- #

    if "self harm" in top_label:
        return {
            "category": "toxic",
            "confidence": confidence
        }

    elif "toxic" in top_label or "abusive" in top_label:
        return {
            "category": "toxic",
            "confidence": confidence
        }

    elif "prompt injection" in top_label:
        return {
            "category": "injection",
            "confidence": confidence
        }

    elif "harmful" in top_label or "dangerous" in top_label:
        return {
            "category": "harmful",
            "confidence": confidence
        }

    else:
        return {
            "category": "safe",
            "confidence": confidence
        }