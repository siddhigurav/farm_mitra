"""
Edge node main application for Raspberry Pi.

Structure:
- `sensors` reads DHT22 and MCP3008 soil sensor
- `vision` captures frames and runs a YOLOv8 detector
- `actuator` triggers a speaker when a large animal is detected
- `mqtt_client` publishes telemetry and detection results and queues while offline

Deployment notes (Raspberry Pi OS):
- Install system deps: `sudo apt update && sudo apt install -y python3-pip python3-venv libatlas-base-dev libopenjp2-7`
- Enable SPI and Camera via `sudo raspi-config` (Interface Options).
- Install Python deps: `pip3 install -r requirements.txt` (may require build time and swap for some packages).
- For best CPU inference performance, convert YOLOv8-nano to ONNX and place at `models/yolov8n.onnx`.

Run:
    sudo python3 main.py

"""
import logging
import threading
import time
import signal
import json
from datetime import datetime

from sensors import read_dht, MCP3008
from vision import Camera, YoloDetector
from actuator import Speaker
from mqtt_client.client import MQTTClient


logging.basicConfig(level=logging.INFO, filename="edge_node.log", filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")


class EdgeNode:
    def __init__(self, config=None):
        self.config = config or {}
        # hardware
        self.dht_pin = self.config.get("dht_pin", 4)
        self.soil_channel = self.config.get("soil_channel", 0)
        self.speaker_pin = self.config.get("speaker_pin", 18)
        # components
        self.soil = MCP3008()
        self.camera = Camera(width=640, height=480, framerate=10)
        self.detector = YoloDetector(model_path=self.config.get("model_path", "models/yolov8n.onnx"))
        self.speaker = Speaker(pin=self.speaker_pin)
        self.mqtt = MQTTClient(broker=self.config.get("mqtt_broker", "localhost"), port=self.config.get("mqtt_port", 1883))
        self.running = False
        self.threads = []

    def start(self):
        self.running = True
        self.mqtt.start()
        t1 = threading.Thread(target=self._sensor_loop, daemon=True)
        t2 = threading.Thread(target=self._vision_loop, daemon=True)
        self.threads.extend([t1, t2])
        for t in self.threads:
            t.start()
        logging.info("EdgeNode started")

    def stop(self):
        self.running = False
        logging.info("Stopping EdgeNode")
        time.sleep(0.5)
        try:
            self.camera.release()
        except Exception:
            pass
        try:
            self.mqtt.stop()
        except Exception:
            pass
        try:
            self.speaker.cleanup()
        except Exception:
            pass

    def _sensor_loop(self):
        while self.running:
            dht = read_dht(self.dht_pin)
            soil = self.soil.read_percent(self.soil_channel)
            payload = {"timestamp": time.time(), "dht": dht, "soil_percent": soil}
            logging.info("Sensors: %s", payload)
            self.mqtt.publish("edge/sensors", payload)
            time.sleep(self.config.get("sensor_interval", 30))

    def _vision_loop(self):
        while self.running:
            frame = self.camera.read()
            if frame is None:
                time.sleep(1)
                continue
            detections = self.detector.detect(frame)
            # simple logic: any detection with area > threshold is considered large
            large = [d for d in detections if d.get("area", 0) > self.config.get("large_area_threshold", 20000)]
            msg = {"timestamp": time.time(), "detections": detections, "large_detected": len(large) > 0}
            logging.info("Vision: %s", json.dumps(msg))
            self.mqtt.publish("edge/vision", msg)
            if len(large) > 0:
                # trigger speaker for configured seconds
                self.speaker.beep(self.config.get("speaker_duration", 5))
            time.sleep(self.config.get("vision_interval", 10))


def _signal_handler(sig, frame, node: EdgeNode = None):
    logging.info("Signal received: %s", sig)
    if node:
        node.stop()
    raise SystemExit(0)


def main():
    node = EdgeNode()
    signal.signal(signal.SIGINT, lambda s, f: _signal_handler(s, f, node))
    signal.signal(signal.SIGTERM, lambda s, f: _signal_handler(s, f, node))
    node.start()
    # keep main thread alive
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
