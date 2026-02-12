from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import os

from analytics.speech_metrics import analyze_speech_from_text
from analytics.text_metrics import analyze_text
from analytics.history import save_attempt, get_history

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Root → open homepage
@app.get("/")
def home():
    return FileResponse("static/index.html")


# ======================
# TEXT EVALUATION
# ======================
class AnswerInput(BaseModel):
    answer: str
    duration: float


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


# ======================
# ANALYTICS API
# ======================
@app.get("/analytics")
def analytics():
    history = get_history()

    return {
        "confidence": [h["confidence"] for h in history],
        "content": [h["content"] for h in history],
        "final": [h["final"] for h in history]
    }


# ======================
# AUDIO UPLOAD
# ======================
@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    return {"filename": file.filename, "status": "Uploaded successfully"}
