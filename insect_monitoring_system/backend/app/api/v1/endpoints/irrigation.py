from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.irrigation import IrrigationApproval
from app.db.models.crop import Crop
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter()

# Pydantic models for request/response
class IrrigationRequest(BaseModel):
    crop_id: int
    duration_minutes: int
    water_amount_liters: int

class IrrigationApprovalCreate(IrrigationRequest):
    pass

class IrrigationApprovalUpdate(BaseModel):
    approved_by_farmer: Optional[bool] = None
    status: Optional[str] = None

class IrrigationApprovalResponse(IrrigationApprovalCreate):
    id: int
    requested_at: datetime
    approved_at: Optional[datetime] = None
    approved_by_farmer: bool
    status: str

    class Config:
        orm_mode = True

@router.get("/irrigation", response_model=List[IrrigationApprovalResponse])
def get_irrigation_approvals(db: Session = Depends(get_db)):
    """
    Get all irrigation approvals
    """
    approvals = db.query(IrrigationApproval).all()
    return approvals

@router.get("/irrigation/{approval_id}", response_model=IrrigationApprovalResponse)
def get_irrigation_approval(approval_id: int, db: Session = Depends(get_db)):
    """
    Get a specific irrigation approval by ID
    """
    approval = db.query(IrrigationApproval).filter(IrrigationApproval.id == approval_id).first()
    if not approval:
        raise HTTPException(status_code=404, detail="Irrigation approval not found")
    return approval

@router.post("/irrigation", response_model=IrrigationApprovalResponse)
def request_irrigation(irrigation: IrrigationApprovalCreate, db: Session = Depends(get_db)):
    """
    Request irrigation for a crop (IoT device initiated)
    """
    # Check if crop exists
    crop = db.query(Crop).filter(Crop.id == irrigation.crop_id).first()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    
    db_irrigation = IrrigationApproval(
        crop_id=irrigation.crop_id,
        duration_minutes=irrigation.duration_minutes,
        water_amount_liters=irrigation.water_amount_liters
    )
    db.add(db_irrigation)
    db.commit()
    db.refresh(db_irrigation)
    return db_irrigation

@router.put("/irrigation/{approval_id}", response_model=IrrigationApprovalResponse)
def update_irrigation_approval(approval_id: int, approval_update: IrrigationApprovalUpdate, db: Session = Depends(get_db)):
    """
    Update irrigation approval (farmer approval)
    """
    db_approval = db.query(IrrigationApproval).filter(IrrigationApproval.id == approval_id).first()
    if not db_approval:
        raise HTTPException(status_code=404, detail="Irrigation approval not found")
    
    # If farmer approves, set approved timestamp
    if approval_update.approved_by_farmer and not db_approval.approved_by_farmer:
        db_approval.approved_at = datetime.utcnow()
    
    for field, value in approval_update.dict(exclude_unset=True).items():
        setattr(db_approval, field, value)
    
    db.commit()
    db.refresh(db_approval)
    return db_approval

@router.delete("/irrigation/{approval_id}")
def delete_irrigation_approval(approval_id: int, db: Session = Depends(get_db)):
    """
    Delete an irrigation approval
    """
    db_approval = db.query(IrrigationApproval).filter(IrrigationApproval.id == approval_id).first()
    if not db_approval:
        raise HTTPException(status_code=404, detail="Irrigation approval not found")
    
    db.delete(db_approval)
    db.commit()
    return {"message": "Irrigation approval deleted successfully"}