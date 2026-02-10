# analytics/text_metrics.py

def analyze_text(text):
    score = min(len(text.split()) / 20, 1.0)
    return {
        "content_score": round(score, 2)
    }
