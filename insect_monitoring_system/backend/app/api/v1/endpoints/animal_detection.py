import shutil
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.animal import Animal
from app.ml_models.animal.detector import detect_animals_from_image
from app.ml_models.animal.alarm import trigger_alarm
import os

router = APIRouter()

@router.post("/detect_animals")
async def detect_animals(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Accepts an image file, detects animals, triggers an alarm if animals are found,
    and saves the detected animal types to the database.
    """
    # Ensure the uploads directory exists
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    # Save the uploaded file temporarily
    temp_file_path = os.path.join(upload_dir, file.filename)
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Perform animal detection
    detection_results = detect_animals_from_image(temp_file_path)

    # Clean up the uploaded file
    os.remove(temp_file_path)

    if detection_results.get("error"):
        return {"error": detection_results["error"]}

    detections = detection_results.get("detections", [])
    
    if not detections:
        return {"status": "No animals detected."}

    # Trigger alarm and save to DB if animals are detected
    trigger_alarm(duration=3)  # Trigger alarm for 3 seconds

    detected_animal_names = set()
    for detection in detections:
        detected_animal_names.add(detection["class_name"])

    # Save new animal types to the database
    for name in detected_animal_names:
        db_animal = db.query(Animal).filter(Animal.name == name).first()
        if not db_animal:
            new_animal = Animal(name=name)
            db.add(new_animal)
    db.commit()

    return {
        "status": "Animals detected and alarm triggered.",
        "detections": detections
    }