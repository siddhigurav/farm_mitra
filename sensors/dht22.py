"""
Simple DHT22 reader.

Notes for Raspberry Pi deployment:
- Install dependency: `sudo apt-get update && sudo apt-get install -y python3-dev python3-pip`
- Install Adafruit library: `pip3 install Adafruit_DHT`
- Use a GPIO pin that supports 1-wire timing; run the script as root or give access to GPIO.
"""
import time
import logging
try:
    import Adafruit_DHT
except Exception:  # pragma: no cover - hardware-specific
    Adafruit_DHT = None


def read_dht(pin: int = 4, retries: int = 3, delay: float = 2.0):
    """Read DHT22 and return dict {temperature_c, humidity, timestamp}.

    pin: BCM GPIO pin number where DHT22 data is connected.
    """
    ts = time.time()
    if Adafruit_DHT is None:
        logging.warning("Adafruit_DHT not available; returning None values")
        return {"temperature_c": None, "humidity": None, "timestamp": ts}

    for _ in range(retries):
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, pin)
        if humidity is not None and temperature is not None:
            return {"temperature_c": round(temperature, 2), "humidity": round(humidity, 2), "timestamp": ts}
        time.sleep(delay)
    return {"temperature_c": None, "humidity": None, "timestamp": ts}
