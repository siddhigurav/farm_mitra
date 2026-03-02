import threading
import json
import logging
import time
from typing import Callable

import paho.mqtt.client as mqtt
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.session import SessionLocal
from app import crud, schemas
from app.api.ws import manager


class MQTTIngestor:
    def __init__(self, broker: str = None, port: int = None, topic: str = None):
        self.broker = broker or settings.MQTT_BROKER
        self.port = port or settings.MQTT_PORT
        self.topic = topic or settings.MQTT_TOPIC
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def start(self):
        t = threading.Thread(target=self._run, daemon=True)
        t.start()

    def _run(self):
        while True:
            try:
                self.client.connect(self.broker, self.port)
                self.client.loop_forever()
            except Exception as e:
                logging.warning("MQTT connect failed: %s", e)
                time.sleep(5)

    def on_connect(self, client, userdata, flags, rc):
        logging.info("MQTT connected rc=%s", rc)
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
        except Exception:
            logging.warning("Invalid JSON payload on %s", msg.topic)
            return
        # determine type from topic or payload
        topic = msg.topic
        db: Session = SessionLocal()
        try:
            if topic.startswith("edge/sensors") or payload.get("type") == "sensor":
                # expected fields: device_uuid, temperature, humidity, soil_percent, raw
                sr = schemas.SensorReadingCreate(**payload)
                db_obj = crud.create_sensor_reading(db, sr)
                manager.broadcast({"type": "sensor", "data": {"id": db_obj.id}})
            elif topic.startswith("edge/vision") or payload.get("type") == "detection":
                ev = schemas.DetectionEventCreate(**payload)
                db_obj = crud.create_detection_event(db, ev)
                manager.broadcast({"type": "detection", "data": {"id": db_obj.id}})
        except Exception as e:
            logging.exception("Error processing MQTT message: %s", e)
        finally:
            db.close()
