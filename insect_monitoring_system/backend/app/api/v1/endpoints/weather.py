from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.weather import Weather
import requests
import os
from datetime import datetime

router = APIRouter()

# Weather API configuration - Open-Meteo (free, no API key required)
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

@router.get("/current_weather")
def get_current_weather(location: str = "Nashik", db: Session = Depends(get_db)):
    """
    Fetches current weather data from Open-Meteo API (free, no API key required).
    """
    try:
        # Default coordinates for common locations
        locations = {
            "Nashik": {"lat": 19.9975, "lon": 73.7898},
            "Mumbai": {"lat": 19.0760, "lon": 72.8777},
            "Pune": {"lat": 18.5204, "lon": 73.8567},
            "Delhi": {"lat": 28.7041, "lon": 77.1025}
        }
        
        coords = locations.get(location, locations["Nashik"])  # Default to Nashik
        
        params = {
            "latitude": coords["lat"],
            "longitude": coords["lon"],
            "current_weather": True,
            "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
            "timezone": "Asia/Kolkata"
        }
        response = requests.get(WEATHER_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # Extract relevant weather data
        current = data["current_weather"]
        weather_data = {
            "location": location,
            "temperature": current["temperature"],
            "humidity": data["hourly"]["relative_humidity_2m"][0] if "hourly" in data else None,
            "pressure": None,  # Open-Meteo doesn't provide pressure in free tier
            "wind_speed": current["wind_speed"],
            "description": get_weather_description(current["weathercode"]),
            "timestamp": datetime.utcnow()
        }

        # Store in database
        weather_entry = Weather(**weather_data)
        db.add(weather_entry)
        db.commit()
        db.refresh(weather_entry)

        return weather_data

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch weather data: {str(e)}")

def get_weather_description(weathercode):
    """Convert Open-Meteo weather codes to descriptions"""
    codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }
    return codes.get(weathercode, "Unknown")

@router.get("/weather_history")
def get_weather_history(limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieves recent weather history from the database.
    """
    weather_records = db.query(Weather).order_by(Weather.timestamp.desc()).limit(limit).all()
    return [
        {
            "id": record.id,
            "location": record.location,
            "temperature": record.temperature,
            "humidity": record.humidity,
            "pressure": record.pressure,
            "wind_speed": record.wind_speed,
            "description": record.description,
            "timestamp": record.timestamp.isoformat()
        }
        for record in weather_records
    ]