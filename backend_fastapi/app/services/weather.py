import httpx
import logging
from datetime import datetime
from app.core.config import settings


def fetch_daily_weather(latitude: float, longitude: float, days: int = 1):
    """Fetch daily weather summary from Open-Meteo and return a dict with min/max temps and precipitation sum.

    Returns:
        {date, min_temp, max_temp, precipitation, raw}
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_min,temperature_2m_max,precipitation_sum",
        "timezone": "UTC",
    }
    with httpx.Client(timeout=10.0) as client:
        r = client.get(settings.OPEN_METEO_URL, params=params)
        r.raise_for_status()
        data = r.json()
    # parse daily arrays, take first day
    try:
        daily = data.get('daily', {})
        date = daily.get('time', [None])[0]
        min_t = daily.get('temperature_2m_min', [None])[0]
        max_t = daily.get('temperature_2m_max', [None])[0]
        precip = daily.get('precipitation_sum', [None])[0]
        return {"date": datetime.fromisoformat(date) if date else datetime.utcnow(), "min_temp": min_t, "max_temp": max_t, "precipitation": precip, "raw": data}
    except Exception as e:
        logging.exception("Failed to parse Open-Meteo response: %s", e)
        return {"date": datetime.utcnow(), "min_temp": None, "max_temp": None, "precipitation": None, "raw": data}
