"""
GPIO-controlled speaker actuator.

Deployment notes:
- Use a GPIO pin driving a transistor or relay to power the speaker/amplifier.
- Do NOT drive a speaker directly from GPIO pin.
"""
import time
import logging

try:
    import RPi.GPIO as GPIO
except Exception:  # pragma: no cover - allow running on non-RPi machines
    GPIO = None


class Speaker:
    def __init__(self, pin: int = 18):
        self.pin = pin
        if GPIO:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.OUT)
        else:
            logging.info("RPi.GPIO not available; speaker will be simulated")

    def beep(self, seconds: float = 5.0):
        logging.info("Speaker beep for %.1fs", seconds)
        if GPIO:
            GPIO.output(self.pin, GPIO.HIGH)
            time.sleep(seconds)
            GPIO.output(self.pin, GPIO.LOW)
        else:
            # simulate by sleeping
            time.sleep(seconds)

    def cleanup(self):
        if GPIO:
            GPIO.cleanup(self.pin)
