from transformers import pipeline

# Zero-shot classifier (fully ML-based)
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Define categories (your taxonomy)
CATEGORIES = [
    "safe normal query",
    "toxic or hate speech",
    "self harm or suicide",
    "prompt injection attack",
    "harmful or dangerous instruction"
]


def classify_prompt(text):
    result = classifier(text, CATEGORIES)

    labels = result["labels"]
    scores = result["scores"]

    top_label = labels[0]
    confidence = float(scores[0])

    # -------- MAP TO YOUR SYSTEM -------- #

    if "self harm" in top_label:
        return {
            "category": "toxic",
            "confidence": confidence
        }

    elif "toxic" in top_label:
        return {
            "category": "toxic",
            "confidence": confidence
        }

    elif "injection" in top_label:
        return {
            "category": "injection",
            "confidence": confidence
        }

    elif "harmful" in top_label:
        return {
            "category": "harmful",
            "confidence": confidence
        }

    else:
        return {
            "category": "safe",
            "confidence": confidence
        }