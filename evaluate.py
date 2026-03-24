import json
from classifier import classify_prompt

thresholds = [0.3, 0.5, 0.7, 0.9]

with open("red_team_dataset.json") as f:
    data = json.load(f)

for THRESHOLD in thresholds:
    correct = 0
    total = len(data)

    for item in data:
        text = item["text"]
        true_label = item["label"]

        pred = classify_prompt(text)
        predicted_label = pred["category"]
        confidence = pred["confidence"]

        if confidence < THRESHOLD:
            predicted_label = "safe"

        if predicted_label == true_label:
            correct += 1

    accuracy = correct / total

    print(f"Threshold: {THRESHOLD} → Accuracy: {accuracy:.2f}")