"""
YOLOv8 detector wrapper.

This module prefers an ONNX runtime inference path for CPU efficiency on Pi.
If `onnxruntime` is not available it will try to use `ultralytics.YOLO` (PyTorch),
which can be heavy on Raspberry Pi. For production on Raspberry Pi, convert a
`yolov8n` model to ONNX and place it at `models/yolov8n.onnx` and ensure
`onnxruntime` is installed.
"""
import logging
import numpy as np
import cv2
from typing import List, Dict

try:
    import onnxruntime as ort
except Exception:  # pragma: no cover - optional
    ort = None

try:
    from ultralytics import YOLO
except Exception:  # pragma: no cover - optional
    YOLO = None


class YoloDetector:
    def __init__(self, model_path: str = "models/yolov8n.onnx", conf_thresh: float = 0.3):
        self.model_path = model_path
        self.conf_thresh = conf_thresh
        self.backend = None
        self.session = None
        self.model = None
        if ort:
            try:
                self.session = ort.InferenceSession(model_path, providers=["CPUExecutionProvider"])
                self.backend = "onnx"
                logging.info("Using ONNX Runtime for inference")
            except Exception:
                self.session = None
        if self.session is None and YOLO:
            try:
                self.model = YOLO(model_path)
                self.backend = "ultralytics"
                logging.info("Using Ultralytics YOLO model")
            except Exception:
                self.model = None
        if self.backend is None:
            logging.warning("No supported model runtime found. Install onnxruntime or ultralytics.")

    def detect(self, frame: np.ndarray) -> List[Dict]:
        """Return list of detections: {label, conf, bbox=[x1,y1,x2,y2], area}
        bbox coordinates are in pixels.
        """
        if frame is None:
            return []
        h, w = frame.shape[:2]
        if self.backend == "onnx" and self.session:
            # Minimal pre/post processing expecting YOLOv8 ONNX export semantics
            img = cv2.resize(frame, (640, 640))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = img.astype(np.float32) / 255.0
            img = np.transpose(img, (2, 0, 1))[None, ...]
            inputs = {self.session.get_inputs()[0].name: img}
            outs = self.session.run(None, inputs)[0]
            # ONNX outputs postprocess is model-specific; here we expect boxes x,y,w,h + conf + class
            detections = []
            for row in outs:
                conf = float(row[4])
                if conf < self.conf_thresh:
                    continue
                # Example layout: cx,cy,w,h,conf,class,score -> requires actual model alignment
                cx, cy, bw, bh = row[0], row[1], row[2], row[3]
                x1 = int((cx - bw / 2) * w)
                y1 = int((cy - bh / 2) * h)
                x2 = int((cx + bw / 2) * w)
                y2 = int((cy + bh / 2) * h)
                cls = int(row[5]) if len(row) > 5 else 0
                detections.append({"label_id": cls, "label": str(cls), "conf": conf, "bbox": [x1, y1, x2, y2], "area": (x2 - x1) * (y2 - y1)})
            return detections

        if self.backend == "ultralytics" and self.model:
            results = self.model(frame)[0]
            detections = []
            for box in results.boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                detections.append({"label_id": cls, "label": str(cls), "conf": conf, "bbox": [x1, y1, x2, y2], "area": (x2 - x1) * (y2 - y1)})
            return detections

        return []
