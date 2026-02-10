import re

def calculate_pronunciation(text: str):
    words = re.findall(r"\b\w+\b", text.lower())
    total_words = len(words)

    if total_words == 0:
        return {
            "clarity_percentage": 0,
            "repeated_words": 0,
            "pronunciation_score": 0
        }

    repeated = sum(1 for i in range(1, total_words) if words[i] == words[i-1])

    clarity = max(0, 100 - (repeated * 5))

    return {
        "clarity_percentage": clarity,
        "repeated_words": repeated,
        "pronunciation_score": clarity
    }
