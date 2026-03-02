from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class Farm(Base):
    __tablename__ = "farms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    location = Column(String, nullable=True)
    devices = relationship("Device", back_populates="farm")


class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    farm_id = Column(Integer, ForeignKey("farms.id"))
    farm = relationship("Farm", back_populates="devices")
    readings = relationship("SensorReading", back_populates="device")
    detections = relationship("DetectionEvent", back_populates="device")


class SensorReading(Base):
    __tablename__ = "sensor_readings"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    soil_percent = Column(Float)
    raw = Column(JSON, nullable=True)
    device = relationship("Device", back_populates="readings")


class DetectionEvent(Base):
    __tablename__ = "detection_events"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    label = Column(String)
    confidence = Column(Float)
    bbox = Column(JSON)
    image_path = Column(String, nullable=True)
    device = relationship("Device", back_populates="detections")


class IrrigationStatus(Base):
    __tablename__ = "irrigation_status"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), index=True)
    enabled = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=datetime.utcnow)
    device = relationship("Device")


class WeatherSummary(Base):
    __tablename__ = "weather_summaries"
    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"), index=True, nullable=True)
    date = Column(DateTime, index=True)
    min_temp = Column(Float, nullable=True)
    max_temp = Column(Float, nullable=True)
    precipitation = Column(Float, nullable=True)
    raw = Column(JSON, nullable=True)
    farm = relationship("Farm")
