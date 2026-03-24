import json
from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_prompts(category, n=5):
    prompt = f"Generate {n} examples of {category} prompts for testing AI safety."

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.choices[0].message.content.split("\n")

    return [t.strip("- ").strip() for t in text if t.strip()]

dataset = []

categories = {
    "harmful": "harmful or dangerous queries",
    "injection": "prompt injection attacks",
    "toxic": "toxic or self-harm content",
    "safe": "normal harmless questions"
}

for label, desc in categories.items():
    prompts = generate_prompts(desc, 5)

    for p in prompts:
        dataset.append({
            "text": p,
            "label": label
        })

# Save dataset
with open("redteam_dataset.json", "w") as f:
    json.dump(dataset, f, indent=2)

print("Dataset generated!")