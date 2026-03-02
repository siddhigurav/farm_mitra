import shutil
import os
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.ml_models.audio.detector import classify_insect_sound

router = APIRouter()

@router.post("/detect_audio")
async def detect_audio(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Accepts an audio file, classifies the insect sound, and returns the result.
    """
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    temp_file_path = os.path.join(upload_dir, file.filename)
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Classify the insect sound
    classification_result = classify_insect_sound(temp_file_path)

    os.remove(temp_file_path)

    if classification_result.get("error"):
        return {"error": classification_result["error"]}

    return {
        "status": "Audio classified.",
        "result": classification_result
    }