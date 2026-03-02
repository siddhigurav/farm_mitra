"""
Camera helper: uses PiCamera when available, falls back to OpenCV VideoCapture.

Raspberry Pi notes:
- For Raspberry Pi OS with libcamera, prefer `libcamera` / `picamera2` APIs.
  This helper tries to use `picamera` first for classic setups; adjust for libcamera.
"""
import logging
import time
import numpy as np
try:
    from picamera import PiCamera
    from picamera.array import PiRGBArray
except Exception:  # pragma: no cover - hardware
    PiCamera = None

import cv2


class Camera:
    def __init__(self, width=640, height=480, framerate=15):
        self.width = width
        self.height = height
        self.framerate = framerate
        self.cam = None
        self._use_picamera = False
        if PiCamera:
            try:
                self.cam = PiCamera()
                self.cam.resolution = (width, height)
                self.cam.framerate = framerate
                self.raw_capture = PiRGBArray(self.cam, size=(width, height))
                time.sleep(0.2)
                self._use_picamera = True
                logging.info("Using PiCamera")
            except Exception:
                self._use_picamera = False
                self.cam = None
        if not self._use_picamera:
            logging.info("Falling back to OpenCV VideoCapture(0)")
            self.cam = cv2.VideoCapture(0)
            self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def read(self):
        """Return a BGR numpy array frame or None."""
        if self._use_picamera:
            self.raw_capture.truncate(0)
            self.cam.capture(self.raw_capture, format="bgr", use_video_port=True)
            frame = self.raw_capture.array
            return frame
        else:
            ok, frame = self.cam.read()
            if not ok:
                logging.warning("Camera read failed")
                return None
            return frame

    def release(self):
        if self._use_picamera and self.cam:
            self.cam.close()
        elif self.cam:
            self.cam.release()
