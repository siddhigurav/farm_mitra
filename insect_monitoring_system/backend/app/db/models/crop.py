import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy import Column, Integer, String, Date, Boolean, Float
from db.base import Base

class Crop(Base):
    __tablename__ = "crops"
    
    id = Column(Integer, primary_key=True, index=True)
    crop_name = Column(String(255), index=True)
    crop_variety = Column(String(255))
    planting_date = Column(Date)
    # Specific attributes for grapes and guava
    expected_harvest_date = Column(Date)
    area_in_hectares = Column(Float)
    irrigation_type = Column(String(255))  # drip, sprinkler, flood
    irrigation_approved = Column(Boolean, default=False)
    last_irrigation_date = Column(Date)
    soil_moisture_level = Column(Float)  # percentage
    ph_level = Column(Float)
    temperature = Column(Float)  # current temperature in Celsius
    humidity = Column(Float)  # percentage