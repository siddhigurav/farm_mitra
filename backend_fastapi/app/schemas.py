from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime


class DeviceBase(BaseModel):
    uuid: str
    name: Optional[str]


class DeviceCreate(DeviceBase):
    pass


class Device(DeviceBase):
    id: int

    class Config:
        orm_mode = True


class SensorReadingBase(BaseModel):
    temperature: Optional[float]
    humidity: Optional[float]
    soil_percent: Optional[float]
    raw: Optional[Any]


class SensorReadingCreate(SensorReadingBase):
    device_uuid: str


class SensorReading(SensorReadingBase):
    id: int
    device_id: int
    timestamp: datetime

    class Config:
        orm_mode = True


class DetectionEventBase(BaseModel):
    label: str
    confidence: float
    bbox: List[int]
    image_path: Optional[str]


class DetectionEventCreate(DetectionEventBase):
    device_uuid: str


class DetectionEvent(DetectionEventBase):
    id: int
    device_id: int
    timestamp: datetime

    class Config:
        orm_mode = True


class IrrigationToggle(BaseModel):
    enabled: bool = Field(...)


class WeatherSummaryBase(BaseModel):
    date: Optional[datetime]
    min_temp: Optional[float]
    max_temp: Optional[float]
    precipitation: Optional[float]
    raw: Optional[Any]


class WeatherSummaryCreate(WeatherSummaryBase):
    farm_id: int


class WeatherSummary(WeatherSummaryBase):
    id: int
    farm_id: int

    class Config:
        orm_mode = True


class Recommendation(BaseModel):
    code: str
    message: str
    severity: str

