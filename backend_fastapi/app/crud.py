from sqlalchemy.orm import Session
from datetime import datetime
from app import models, schemas


def get_or_create_device(db: Session, uuid: str, name: str = None):
    device = db.query(models.Device).filter(models.Device.uuid == uuid).first()
    if device:
        return device
    device = models.Device(uuid=uuid, name=name)
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


def create_sensor_reading(db: Session, reading: schemas.SensorReadingCreate):
    device = get_or_create_device(db, uuid=reading.device_uuid)
    sr = models.SensorReading(device_id=device.id, temperature=reading.temperature,
                              humidity=reading.humidity, soil_percent=reading.soil_percent,
                              raw=reading.raw, timestamp=datetime.utcnow())
    db.add(sr)
    db.commit()
    db.refresh(sr)
    return sr


def create_detection_event(db: Session, event: schemas.DetectionEventCreate):
    device = get_or_create_device(db, uuid=event.device_uuid)
    ev = models.DetectionEvent(device_id=device.id, label=event.label, confidence=event.confidence,
                               bbox=event.bbox, image_path=event.image_path, timestamp=datetime.utcnow())
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return ev


def toggle_irrigation(db: Session, device_uuid: str, enabled: bool):
    device = get_or_create_device(db, uuid=device_uuid)
    status = db.query(models.IrrigationStatus).filter(models.IrrigationStatus.device_id == device.id).first()
    if not status:
        status = models.IrrigationStatus(device_id=device.id, enabled=enabled, updated_at=datetime.utcnow())
        db.add(status)
    else:
        status.enabled = enabled
        status.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(status)
    return status


def get_latest_readings(db: Session, limit: int = 100):
    # return latest N readings across devices
    return db.query(models.SensorReading).order_by(models.SensorReading.timestamp.desc()).limit(limit).all()


def get_detection_history(db: Session, device_uuid: str = None, limit: int = 100):
    q = db.query(models.DetectionEvent).order_by(models.DetectionEvent.timestamp.desc())
    if device_uuid:
        device = db.query(models.Device).filter(models.Device.uuid == device_uuid).first()
        if device:
            q = q.filter(models.DetectionEvent.device_id == device.id)
        else:
            return []
    return q.limit(limit).all()


def get_farm(db: Session, farm_id: int):
    return db.query(models.Farm).filter(models.Farm.id == farm_id).first()


def create_weather_summary(db: Session, farm_id: int, date, min_temp: float = None, max_temp: float = None, precipitation: float = None, raw: dict = None):
    ws = models.WeatherSummary(farm_id=farm_id, date=date, min_temp=min_temp, max_temp=max_temp, precipitation=precipitation, raw=raw)
    db.add(ws)
    db.commit()
    db.refresh(ws)
    return ws


def get_latest_weather_for_farm(db: Session, farm_id: int):
    return db.query(models.WeatherSummary).filter(models.WeatherSummary.farm_id == farm_id).order_by(models.WeatherSummary.date.desc()).first()


def get_latest_sensor_for_farm(db: Session, farm_id: int):
    # find latest sensor reading across devices for the farm
    return db.query(models.SensorReading).join(models.Device).filter(models.Device.farm_id == farm_id).order_by(models.SensorReading.timestamp.desc()).first()
