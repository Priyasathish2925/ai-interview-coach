import json
import os

HISTORY_FILE = os.path.join(os.path.dirname(__file__), "history.json")

print("HISTORY FILE PATH:", HISTORY_FILE)

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)

def save_attempt(attempt):
    history = load_history()

    attempt["attempt"] = len(history) + 1
    history.append(attempt)

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

    print("🔥 SAVE_ATTEMPT FUNCTION CALLED 🔥")

def get_history():
    return load_history()
