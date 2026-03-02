import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from db.base import Base
import datetime

class RemedyApproval(Base):
    __tablename__ = "remedy_approvals"
    
    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"))
    insect_id = Column(Integer, ForeignKey("insects.id"))
    remedy_type = Column(String(255))  # pesticide, organic, biological, etc.
    remedy_name = Column(String(255))  # Specific product name
    description = Column(String(500))
    requested_at = Column(DateTime, default=datetime.datetime.utcnow)
    approved_at = Column(DateTime, nullable=True)
    approved_by_farmer = Column(Boolean, default=False)
    status = Column(String(50), default="pending")  # pending, approved, completed, rejected