from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.crop import Crop
from app.db.models.irrigation import IrrigationApproval
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter()

# Pydantic models for IoT device data
class SensorData(BaseModel):
    crop_id: int
    soil_moisture_level: float
    ph_level: float
    temperature: float
    humidity: float

class IrrigationRequestData(BaseModel):
    crop_id: int
    duration_minutes: int
    water_amount_liters: int
    reason: str  # e.g., "low_soil_moisture", "scheduled_irrigation"

@router.post("/iot/sensor_data")
def update_sensor_data(sensor_data: SensorData, db: Session = Depends(get_db)):
    """
    Update crop conditions based on IoT sensor data
    """
    # Get crop information
    crop = db.query(Crop).filter(Crop.id == sensor_data.crop_id).first()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    
    # Update crop conditions
    crop.soil_moisture_level = sensor_data.soil_moisture_level
    crop.ph_level = sensor_data.ph_level
    crop.temperature = sensor_data.temperature
    crop.humidity = sensor_data.humidity
    crop.last_irrigation_date = datetime.utcnow().date() if crop.last_irrigation_date is None else crop.last_irrigation_date
    
    db.commit()
    db.refresh(crop)
    
    # Check if irrigation is needed based on soil moisture
    irrigation_needed = False
    irrigation_reason = ""
    
    if sensor_data.soil_moisture_level < 30.0:  # Below 30% moisture
        irrigation_needed = True
        irrigation_reason = "Low soil moisture level detected"
    elif sensor_data.soil_moisture_level > 80.0:  # Above 80% moisture
        irrigation_reason = "High soil moisture level detected - irrigation may not be needed"
    
    return {
        "status": "Sensor data updated successfully",
        "crop_id": crop.id,
        "irrigation_needed": irrigation_needed,
        "irrigation_reason": irrigation_reason,
        "updated_conditions": {
            "soil_moisture_level": crop.soil_moisture_level,
            "ph_level": crop.ph_level,
            "temperature": crop.temperature,
            "humidity": crop.humidity
        }
    }

@router.post("/iot/request_irrigation")
def request_irrigation(irrigation_request: IrrigationRequestData, db: Session = Depends(get_db)):
    """
    Request irrigation based on IoT device analysis
    """
    # Get crop information
    crop = db.query(Crop).filter(Crop.id == irrigation_request.crop_id).first()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    
    # Create irrigation approval request
    db_irrigation = IrrigationApproval(
        crop_id=irrigation_request.crop_id,
        duration_minutes=irrigation_request.duration_minutes,
        water_amount_liters=irrigation_request.water_amount_liters,
        status="pending"
    )
    db.add(db_irrigation)
    db.commit()
    db.refresh(db_irrigation)
    
    return {
        "status": "Irrigation request submitted",
        "approval_id": db_irrigation.id,
        "crop_id": irrigation_request.crop_id,
        "duration_minutes": irrigation_request.duration_minutes,
        "water_amount_liters": irrigation_request.water_amount_liters,
        "reason": irrigation_request.reason
    }

@router.get("/iot/crop_conditions/{crop_id}")
def get_crop_conditions(crop_id: int, db: Session = Depends(get_db)):
    """
    Get current crop conditions from IoT sensors
    """
    crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    
    return {
        "crop_id": crop.id,
        "crop_name": crop.crop_name,
        "crop_variety": crop.crop_variety,
        "conditions": {
            "soil_moisture_level": crop.soil_moisture_level,
            "ph_level": crop.ph_level,
            "temperature": crop.temperature,
            "humidity": crop.humidity,
            "last_irrigation_date": crop.last_irrigation_date
        },
        "irrigation_status": "Irrigation needed" if (crop.soil_moisture_level and crop.soil_moisture_level < 30.0) else "Optimal conditions"
    }