import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./insect_monitoring.db")
    
    # Weather API configuration
    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY", "your_weather_api_key_here")
    WEATHER_API_URL: str = os.getenv("WEATHER_API_URL", "http://api.openweathermap.org/data/2.5/weather")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "smart_farming_secret_key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()