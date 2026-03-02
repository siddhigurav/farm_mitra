from sqlalchemy import Column, Integer, String, DateTime, Float
from app.db.base import Base
import datetime

class Weather(Base):
    __tablename__ = "weather"
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String(255), index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    pressure = Column(Float)
    wind_speed = Column(Float)
    description = Column(String(255))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)