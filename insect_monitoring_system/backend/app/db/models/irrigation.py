from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from app.db.base import Base
import datetime

class IrrigationApproval(Base):
    __tablename__ = "irrigation_approvals"
    
    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"))
    requested_at = Column(DateTime, default=datetime.datetime.utcnow)
    approved_at = Column(DateTime, nullable=True)
    approved_by_farmer = Column(Boolean, default=False)
    duration_minutes = Column(Integer)  # How long to irrigate
    water_amount_liters = Column(Integer)  # How much water to use
    status = Column(String(50), default="pending")  # pending, approved, completed, rejected