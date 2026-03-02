from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.db.session import get_db
from app.api.ws import manager
import httpx
from app.core.config import settings
from app import crud
from app.services import weather as weather_service
from app.rules import evaluate_rules
from datetime import datetime

router = APIRouter()


@router.get("/sensors/latest", response_model=List[schemas.SensorReading])
def latest_sensors(limit: int = 50, db: Session = Depends(get_db)):
    return crud.get_latest_readings(db, limit=limit)


@router.get("/detections", response_model=List[schemas.DetectionEvent])
def detections(device_uuid: str = None, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_detection_history(db, device_uuid=device_uuid, limit=limit)


@router.post("/irrigation/{device_uuid}")
def toggle_irrigation(device_uuid: str, toggle: schemas.IrrigationToggle, db: Session = Depends(get_db)):
    status = crud.toggle_irrigation(db, device_uuid, toggle.enabled)
    # broadcast change
    manager.broadcast({"type": "irrigation", "device_uuid": device_uuid, "enabled": status.enabled})
    return {"status": "ok", "enabled": status.enabled}


@router.get("/weather")
def get_weather(lat: float, lon: float):
    params = {"latitude": lat, "longitude": lon, "hourly": "temperature_2m,relativehumidity_2m"}
    with httpx.Client() as client:
        r = client.get(settings.OPEN_METEO_URL, params=params, timeout=10.0)
        r.raise_for_status()
        return r.json()


@router.get("/farm/{farm_id}/recommendations", response_model=List[dict])
def farm_recommendations(farm_id: int, db: Session = Depends(get_db)):
    farm = crud.get_farm(db, farm_id)
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")

    # latest sensor reading for the farm
    latest_sensor = crud.get_latest_sensor_for_farm(db, farm_id)

    # latest weather summary; if missing or older than today, attempt fetch if farm has location
    weather = crud.get_latest_weather_for_farm(db, farm_id)
    # try to fetch if no weather and farm.location looks like 'lat,lon'
    if (not weather or (weather and weather.date.date() != datetime.utcnow().date())) and farm.location:
        try:
            latlon = [s.strip() for s in farm.location.split(',')]
            lat, lon = float(latlon[0]), float(latlon[1])
            w = weather_service.fetch_daily_weather(lat, lon)
            weather = crud.create_weather_summary(db, farm_id=farm.id, date=w.get('date'), min_temp=w.get('min_temp'), max_temp=w.get('max_temp'), precipitation=w.get('precipitation'), raw=w.get('raw'))
        except Exception:
            # ignore fetch errors and proceed with whatever data we have
            pass

    recs = evaluate_rules(latest_sensor, weather)
    return recs
