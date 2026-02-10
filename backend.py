from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil
import uuid

from analytics.speech_metrics import analyze_speech_from_text
from analytics.text_metrics import analyze_text
from fastapi.responses import JSONResponse
from analytics.history import save_attempt, get_history
from fastapi.staticfiles import StaticFiles



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)


class AnswerInput(BaseModel):
    answer: str
    duration: float


@app.get("/")
def home():
    return {"message": "AI Interview Coach API running 🚀"}


# ======================
# TEXT EVALUATION
# ======================
@app.post("/evaluate")
def evaluate(data: AnswerInput):
    speech = analyze_speech_from_text(data.answer, data.duration)
    text = analyze_text(data.answer)

    final_score = round(
        (speech["confidence_score"] * 0.6) +
        (text["content_score"] * 40),
        2
    )

    attempt = {
        "confidence": speech["confidence_score"],
        "content": text["content_score"],
        "final": final_score
    }

    save_attempt(attempt)

    return {
        "speech_metrics": speech,
        "text_metrics": text,
        "final_score": final_score
    }

# ======================
# HISTORY
# ======================
@app.get("/history")
def history_data():
    return get_history()

# =====================
# Confidence graph API
# =====================
@app.get("/confidence-graph")
def confidence_graph():
    history = get_history()
    return [
        {
            "attempt": i + 1,
            "confidence": h["confidence"]
        }
        for i, h in enumerate(history)
    ]
from fastapi.responses import FileResponse

@app.get("/confidence-graph")
def confidence_graph():
    history = get_history()

    if len(history) == 0:
        return {"message": "No data to plot"}

    confidences = [h["confidence"] for h in history]
    attempts = list(range(1, len(confidences) + 1))

    plt.figure()
    plt.plot(attempts, confidences)
    plt.xlabel("Attempt")
    plt.ylabel("Confidence")
    plt.title("Confidence Progress")

    file_path = "confidence_graph.png"
    plt.savefig(file_path)
    plt.close()

    return FileResponse(file_path, media_type="image/png")
@app.get("/confidence-graph")
def confidence_graph():
    history = get_history()

    if not history:
        return JSONResponse(content={
            "x": [],
            "y": []
        })

    x = [item["attempt"] for item in history]
    y = [item["confidence"] for item in history]

    return JSONResponse(content={
        "x": x,
        "y": y
    })
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/analytics")
def analytics():
    history = get_history()

    return {
        "attempts": [h["attempt"] for h in history],
        "confidence": [h["confidence"] for h in history],
        "content": [h["content"] for h in history],
        "final": [h["final"] for h in history]
    }
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from fastapi.responses import FileResponse

@app.get("/report")
def generate_report():
    history = get_history()

    file_path = "interview_report.pdf"
    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    content = [Paragraph("<b>Interview Progress Report</b>", styles["Title"])]

    for h in history:
        text = f"""
        Attempt {h.get('attempt')}<br/>
        Confidence: {h.get('confidence')}<br/>
        Content: {h.get('content')}<br/>
        Final Score: {h.get('final')}<br/><br/>
        """
        content.append(Paragraph(text, styles["Normal"]))

    doc.build(content)

    return FileResponse(file_path, filename="Interview_Report.pdf")
from fastapi.responses import RedirectResponse

@app.get("/")
def root():
    return RedirectResponse(url="/static/dashboard.html")
