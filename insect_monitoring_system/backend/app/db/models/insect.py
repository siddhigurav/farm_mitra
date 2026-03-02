import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy import Column, Integer, String, Float, Boolean
from db.base import Base

class Insect(Base):
    __tablename__ = "insects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    density = Column(Float)
    # Classification for grapes and guava
    is_harmful = Column(Boolean, default=True)  # True if harmful, False if useful
    crop_type = Column(String(255))  # grapes, guava, or general
    recommended_action = Column(String(255))  # What to do about this insect