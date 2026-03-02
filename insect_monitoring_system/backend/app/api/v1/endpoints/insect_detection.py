import shutil
import os
from fastapi import APIRouter, Depends, File, UploadFile, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.insect import Insect
from app.db.models.crop import Crop
from app.db.models.remedy import RemedyApproval
from app.ml_models.insect.detector import detect_insects_from_image
from app.ml_models.insect.coverage import calculate_area_coverage

router = APIRouter()

@router.post("/detect_insects")
async def detect_insects(
    file: UploadFile = File(...), 
    crop_id: int = Query(..., description="ID of the crop being monitored"),
    db: Session = Depends(get_db)
):
    """
    Accepts an image, detects insects, calculates infestation density,
    and stores the data in the database. Also generates remedy recommendations
    based on crop type and insect classification.
    """
    # Get crop information
    crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if not crop:
        return {"error": "Crop not found"}
    
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    temp_file_path = os.path.join(upload_dir, file.filename)
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Detect insects and calculate area coverage
    detection_results = detect_insects_from_image(temp_file_path, crop.crop_name.lower())
    coverage_results = calculate_area_coverage(temp_file_path)

    os.remove(temp_file_path)

    if detection_results.get("error") or coverage_results.get("error"):
        return {"error": detection_results.get("error") or coverage_results.get("error")}

    detections = detection_results.get("detections", [])
    coverage = coverage_results.get("coverage_percentage", 0)

    if not detections:
        return {"status": "No insects detected."}

    # Group by insect name and count
    insect_counts = {}
    harmful_insects_detected = []
    
    for det in detections:
        name = det["class_name"]
        insect_counts[name] = insect_counts.get(name, 0) + 1
        
        # Track harmful insects for remedy recommendations
        if det["is_harmful"]:
            harmful_insects_detected.append(det)

    # Save or update insect data
    for name, count in insect_counts.items():
        # Find detection info for this insect
        insect_detection = next((d for d in detections if d["class_name"] == name), None)
        
        db_insect = db.query(Insect).filter(Insect.name == name).first()
        if db_insect:
            # Simple average for density, could be more complex
            db_insect.density = (db_insect.density + coverage) / 2
            # Update harmful classification if needed
            if insect_detection:
                db_insect.is_harmful = insect_detection["is_harmful"]
                db_insect.crop_type = insect_detection["crop_type"]
                db_insect.recommended_action = insect_detection["recommended_action"]
        else:
            db_insect = Insect(
                name=name, 
                density=coverage,
                is_harmful=insect_detection["is_harmful"] if insect_detection else True,
                crop_type=insect_detection["crop_type"] if insect_detection else "general",
                recommended_action=insect_detection["recommended_action"] if insect_detection else "Monitor"
            )
            db.add(db_insect)
    
    db.commit()

    # Generate remedy recommendations for harmful insects
    remedy_recommendations = []
    for insect_info in harmful_insects_detected:
        # Create remedy approval requests for harmful insects
        remedy = RemedyApproval(
            crop_id=crop_id,
            insect_id=db_insect.id if db_insect else None,
            remedy_type="pesticide" if insect_info["recommended_action"] else "organic",
            remedy_name=f"Targeted treatment for {insect_info['class_name']}",
            description=insect_info["recommended_action"]
        )
        db.add(remedy)
        remedy_recommendations.append({
            "insect": insect_info["class_name"],
            "is_harmful": insect_info["is_harmful"],
            "recommended_action": insect_info["recommended_action"]
        })
    
    db.commit()

    return {
        "status": f"{len(detections)} insects detected.",
        "crop": crop.crop_name,
        "insect_counts": insect_counts,
        "infestation_density_percentage": coverage,
        "remedy_recommendations": remedy_recommendations
    }