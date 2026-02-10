import re

FILLER_WORDS = ["uh", "um", "ah", "like", "you know", "actually"]

def calculate_confidence(text: str, duration: int):
    words = text.lower().split()
    word_count = len(words)

    # Words per second
    wps = word_count / max(duration, 1)

    # Ideal speaking speed: 2–3 words/sec
    if 2 <= wps <= 3:
        speed_score = 100
    elif 1.5 <= wps < 2 or 3 < wps <= 3.5:
        speed_score = 75
    else:
        speed_score = 50

    # Filler word count
    filler_count = sum(text.lower().count(fw) for fw in FILLER_WORDS)

    filler_penalty = min(filler_count * 10, 40)

    confidence_score = max(0, speed_score - filler_penalty)

    return {
        "words_per_second": round(wps, 2),
        "filler_words": filler_count,
        "confidence_score": confidence_score
    }
