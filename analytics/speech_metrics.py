# analytics/speech_metrics.py

def analyze_speech_from_text(text, duration):
    words = text.split()
    word_count = len(words)
    wpm = (word_count / duration) * 60 if duration > 0 else 0

    filler_words = sum(
        text.lower().count(w) for w in ["um", "uh", "like"]
    )

    confidence_score = min(1.0, wpm / 150)

    return {
        "word_count": word_count,
        "words_per_minute": round(wpm, 2),
        "filler_words": filler_words,
        "confidence_score": round(confidence_score, 2)
    }
