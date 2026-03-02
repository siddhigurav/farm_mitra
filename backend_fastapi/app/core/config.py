try:
    from pydantic import BaseSettings
except Exception:
    from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/iot_db"
    MQTT_BROKER: str = "localhost"
    MQTT_PORT: int = 1883
    MQTT_TOPIC: str = "edge/#"
    OPEN_METEO_URL: str = "https://api.open-meteo.com/v1/forecast"

    class Config:
        env_file = ".env"


settings = Settings()
