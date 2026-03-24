import re

def detect_prompt_injection(text):
    patterns = [
        r"ignore previous instructions",
        r"act as",
        r"bypass",
        r"jailbreak",
        r"pretend to be"
    ]

    for p in patterns:
        if re.search(p, text.lower()):
            return True, p  # return pattern matched

    return False, None


def detect_harmful(text):
    harmful_keywords = [
        "kill", "hack", "attack", "bomb", "drugs", "weapon"
    ]

    for word in harmful_keywords:
        if word in text.lower():
            return True, word  # return matched keyword

    return False, None


def restrict_domain(text):
    restricted_topics = ["medical", "legal advice"]

    for topic in restricted_topics:
        if topic in text.lower():
            return True, topic

    return False, None


def output_filter(text):
    blocked_words = ["hate", "violence"]

    for word in blocked_words:
        if word in text.lower():
            return f"Response blocked due to unsafe content (keyword: {word})"

    return text