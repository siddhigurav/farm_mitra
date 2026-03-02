from typing import List

def evaluate_rules(latest_sensor, weather_summary, thresholds=None) -> List[dict]:
    """Return a list of recommendations (dict with code, message, severity).

    latest_sensor: SensorReading ORM or dict with temperature, humidity, soil_percent
    weather_summary: WeatherSummary ORM or dict with precipitation
    thresholds: dict overriding default thresholds
    """
    thresholds = thresholds or {}
    soil_threshold = thresholds.get('soil_percent', 30.0)
    high_humidity = thresholds.get('humidity_high', 75.0)
    high_temp = thresholds.get('temp_high', 30.0)
    rain_precip = thresholds.get('rain_precip', 2.0)  # mm

    recs = []
    # 1. moisture < threshold -> suggest irrigation
    soil = None
    if latest_sensor:
        soil = getattr(latest_sensor, 'soil_percent', None) if not isinstance(latest_sensor, dict) else latest_sensor.get('soil_percent')
    if soil is not None and soil < soil_threshold:
        recs.append({"code": "irrigation_suggest", "message": f"Soil moisture low ({soil}%). Consider irrigation.", "severity": "high"})

    # 2. humidity high + temp high -> fungal risk
    hum = None
    temp = None
    if latest_sensor:
        hum = getattr(latest_sensor, 'humidity', None) if not isinstance(latest_sensor, dict) else latest_sensor.get('humidity')
        temp = getattr(latest_sensor, 'temperature', None) if not isinstance(latest_sensor, dict) else latest_sensor.get('temperature')
    if hum is not None and temp is not None and hum >= high_humidity and temp >= high_temp:
        recs.append({"code": "fungal_risk", "message": "High humidity and temperature detected — increased fungal risk.", "severity": "medium"})

    # 3. rain forecast -> suggest skip irrigation
    precip = None
    if weather_summary:
        precip = getattr(weather_summary, 'precipitation', None) if not isinstance(weather_summary, dict) else weather_summary.get('precipitation')
    if precip is not None and precip >= rain_precip:
        recs.append({"code": "skip_irrigation", "message": f"Rain forecast ({precip}mm). Consider skipping irrigation.", "severity": "low"})

    return recs
