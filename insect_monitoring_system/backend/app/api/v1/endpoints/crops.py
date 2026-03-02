from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.crop import Crop
from app.db.models.insect import Insect
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

router = APIRouter()

# Pydantic models for request/response
class CropCreate(BaseModel):
    crop_name: str
    crop_variety: str
    planting_date: date
    expected_harvest_date: Optional[date] = None
    area_in_hectares: float
    irrigation_type: str

class CropUpdate(BaseModel):
    crop_name: Optional[str] = None
    crop_variety: Optional[str] = None
    planting_date: Optional[date] = None
    expected_harvest_date: Optional[date] = None
    area_in_hectares: Optional[float] = None
    irrigation_type: Optional[str] = None
    irrigation_approved: Optional[bool] = None
    last_irrigation_date: Optional[date] = None
    soil_moisture_level: Optional[float] = None
    ph_level: Optional[float] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None

class CropResponse(CropCreate):
    id: int
    irrigation_approved: bool
    last_irrigation_date: Optional[date] = None
    soil_moisture_level: Optional[float] = None
    ph_level: Optional[float] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None

    class Config:
        orm_mode = True

@router.get("/crops", response_model=List[CropResponse])
def get_crops(db: Session = Depends(get_db)):
    """
    Get all crops
    """
    crops = db.query(Crop).all()
    return crops

@router.get("/crops/{crop_id}", response_model=CropResponse)
def get_crop(crop_id: int, db: Session = Depends(get_db)):
    """
    Get a specific crop by ID
    """
    crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    return crop

@router.post("/crops", response_model=CropResponse)
def create_crop(crop: CropCreate, db: Session = Depends(get_db)):
    """
    Create a new crop
    """
    db_crop = Crop(
        crop_name=crop.crop_name,
        crop_variety=crop.crop_variety,
        planting_date=crop.planting_date,
        expected_harvest_date=crop.expected_harvest_date,
        area_in_hectares=crop.area_in_hectares,
        irrigation_type=crop.irrigation_type
    )
    db.add(db_crop)
    db.commit()
    db.refresh(db_crop)
    return db_crop

@router.put("/crops/{crop_id}", response_model=CropResponse)
def update_crop(crop_id: int, crop_update: CropUpdate, db: Session = Depends(get_db)):
    """
    Update a crop
    """
    db_crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if not db_crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    
    for field, value in crop_update.dict(exclude_unset=True).items():
        setattr(db_crop, field, value)
    
    db.commit()
    db.refresh(db_crop)
    return db_crop

@router.delete("/crops/{crop_id}")
def delete_crop(crop_id: int, db: Session = Depends(get_db)):
    """
    Delete a crop
    """
    db_crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if not db_crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    
    db.delete(db_crop)
    db.commit()
    return {"message": "Crop deleted successfully"}