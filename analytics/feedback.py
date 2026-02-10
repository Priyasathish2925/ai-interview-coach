def generate_feedback(score, confidence, pronunciation):
    feedback = []

    # Content
    if score["content_score"] < 40:
        feedback.append("Try to add more details and examples to strengthen your answer.")
    else:
        feedback.append("Your answer content is relevant and clear.")

    # Fluency
    if score["fluency_score"] < 60:
        feedback.append("Work on reducing pauses and filler words for smoother delivery.")
    else:
        feedback.append("Your speech fluency is very good.")

    # Confidence
    if confidence["confidence_score"] < 60:
        feedback.append("Speak a little louder and maintain a steady pace to sound more confident.")
    else:
        feedback.append("You sound confident and composed.")

    # Pronunciation
    if pronunciation["pronunciation_score"] < 70:
        feedback.append("Focus on clear pronunciation, especially at the end of sentences.")
    else:
        feedback.append("Your pronunciation is clear and understandable.")

    return " ".join(feedback)
