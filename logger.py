import json
from datetime import datetime

LOG_FILE = "logs.json"

def log_event(user_input, response, status):
    log = {
        "timestamp": str(datetime.now()),
        "input": user_input,
        "response": response,
        "status": status
    }

    try:
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(log)

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)