"""
MQTT Client with local queueing when offline.

Uses `paho.mqtt.client`. Stores queued messages in a small SQLite database
so messages are persisted across reboots when the broker is unreachable.
"""
import json
import logging
import sqlite3
import threading
import time
from typing import Any

import paho.mqtt.client as mqtt


class MQTTClient:
    def __init__(self, broker: str = "localhost", port: int = 1883, queue_db: str = "mqtt_queue.db"):
        self.broker = broker
        self.port = port
        self.client = mqtt.Client()
        self.connected = False
        self.lock = threading.Lock()
        self.queue_db = queue_db
        self._init_db()
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect

    def _init_db(self):
        self.conn = sqlite3.connect(self.queue_db, check_same_thread=False)
        cur = self.conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS queue (id INTEGER PRIMARY KEY, topic TEXT, payload TEXT, ts REAL)""")
        self.conn.commit()

    def start(self):
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        while True:
            try:
                if not self.connected:
                    logging.info("Connecting to MQTT broker %s:%d", self.broker, self.port)
                    self.client.connect(self.broker, self.port)
                    self.client.loop_start()
                else:
                    # flush queue periodically
                    self._flush_queue()
                time.sleep(5)
            except Exception as e:
                logging.warning("MQTT loop error: %s", e)
                time.sleep(5)

    def _on_connect(self, client, userdata, flags, rc):
        logging.info("Connected to MQTT (rc=%s)", rc)
        self.connected = True
        # flush queued messages when connected
        self._flush_queue()

    def _on_disconnect(self, client, userdata, rc):
        logging.warning("MQTT disconnected (rc=%s)", rc)
        self.connected = False

    def publish(self, topic: str, payload: Any):
        payload_str = json.dumps(payload)
        if self.connected:
            try:
                self.client.publish(topic, payload_str)
                return True
            except Exception as e:
                logging.warning("Publish failed, queueing: %s", e)
        # queue locally
        with self.lock:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO queue (topic, payload, ts) VALUES (?, ?, ?)", (topic, payload_str, time.time()))
            self.conn.commit()
        return False

    def _flush_queue(self):
        with self.lock:
            cur = self.conn.cursor()
            rows = cur.execute("SELECT id, topic, payload FROM queue ORDER BY id ASC LIMIT 50").fetchall()
            for _id, topic, payload in rows:
                try:
                    self.client.publish(topic, payload)
                    cur.execute("DELETE FROM queue WHERE id=?", (_id,))
                    self.conn.commit()
                except Exception as e:
                    logging.warning("Failed to flush queued message %s: %s", _id, e)
                    break

    def stop(self):
        try:
            self.client.loop_stop()
            self.client.disconnect()
        except Exception:
            pass
