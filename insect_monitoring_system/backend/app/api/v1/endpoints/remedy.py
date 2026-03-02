from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.remedy import RemedyApproval
from app.db.models.crop import Crop
from app.db.models.insect import Insect
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter()

# Pydantic models for request/response
class RemedyRequest(BaseModel):
    crop_id: int
    insect_id: int
    remedy_type: str
    remedy_name: str
    description: str

class RemedyApprovalCreate(RemedyRequest):
    pass

class RemedyApprovalUpdate(BaseModel):
    approved_by_farmer: Optional[bool] = None
    status: Optional[str] = None

class RemedyApprovalResponse(RemedyApprovalCreate):
    id: int
    requested_at: datetime
    approved_at: Optional[datetime] = None
    approved_by_farmer: bool
    status: str

    class Config:
        orm_mode = True

@router.get("/remedy", response_model=List[RemedyApprovalResponse])
def get_remedy_approvals(db: Session = Depends(get_db)):
    """
    Get all remedy approvals
    """
    approvals = db.query(RemedyApproval).all()
    return approvals

@router.get("/remedy/{approval_id}", response_model=RemedyApprovalResponse)
def get_remedy_approval(approval_id: int, db: Session = Depends(get_db)):
    """
    Get a specific remedy approval by ID
    """
    approval = db.query(RemedyApproval).filter(RemedyApproval.id == approval_id).first()
    if not approval:
        raise HTTPException(status_code=404, detail="Remedy approval not found")
    return approval

@router.post("/remedy", response_model=RemedyApprovalResponse)
def request_remedy(remedy: RemedyApprovalCreate, db: Session = Depends(get_db)):
    """
    Request remedy for a crop-insect combination (IoT device initiated)
    """
    # Check if crop exists
    crop = db.query(Crop).filter(Crop.id == remedy.crop_id).first()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    
    # Check if insect exists
    insect = db.query(Insect).filter(Insect.id == remedy.insect_id).first()
    if not insect:
        raise HTTPException(status_code=404, detail="Insect not found")
    
    db_remedy = RemedyApproval(
        crop_id=remedy.crop_id,
        insect_id=remedy.insect_id,
        remedy_type=remedy.remedy_type,
        remedy_name=remedy.remedy_name,
        description=remedy.description
    )
    db.add(db_remedy)
    db.commit()
    db.refresh(db_remedy)
    return db_remedy

@router.put("/remedy/{approval_id}", response_model=RemedyApprovalResponse)
def update_remedy_approval(approval_id: int, approval_update: RemedyApprovalUpdate, db: Session = Depends(get_db)):
    """
    Update remedy approval (farmer approval)
    """
    db_approval = db.query(RemedyApproval).filter(RemedyApproval.id == approval_id).first()
    if not db_approval:
        raise HTTPException(status_code=404, detail="Remedy approval not found")
    
    # If farmer approves, set approved timestamp
    if approval_update.approved_by_farmer and not db_approval.approved_by_farmer:
        db_approval.approved_at = datetime.utcnow()
    
    for field, value in approval_update.dict(exclude_unset=True).items():
        setattr(db_approval, field, value)
    
    db.commit()
    db.refresh(db_approval)
    return db_approval

@router.delete("/remedy/{approval_id}")
def delete_remedy_approval(approval_id: int, db: Session = Depends(get_db)):
    """
    Delete a remedy approval
    """
    db_approval = db.query(RemedyApproval).filter(RemedyApproval.id == approval_id).first()
    if not db_approval:
        raise HTTPException(status_code=404, detail="Remedy approval not found")
    
    db.delete(db_approval)
    db.commit()
    return {"message": "Remedy approval deleted successfully"}