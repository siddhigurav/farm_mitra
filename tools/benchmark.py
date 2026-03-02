"""
Benchmark ONNX/OpenVINO YOLOv8-nano inference on CPU.

Features:
- Runs inference using ONNX Runtime or OpenVINO (if available).
- Measures FPS, per-frame latency, CPU usage via psutil.
- Applies confidence threshold.
- Implements cooldown to prevent repeated triggering.
- Saves detection images to `detections/` with timestamp.
- Logs performance to CSV.

Usage:
    python tools/benchmark.py --model models/yolov8n.onnx --backend onnxruntime --source 0

Notes:
- On Raspberry Pi use `--source 0` for camera (ensure camera driver), or pass a video/file path.
"""
import argparse
import time
import os
import csv
import logging
from collections import deque
from datetime import datetime

import cv2
import numpy as np
import psutil

try:
    import onnxruntime as ort
except Exception:
    ort = None

try:
    from openvino.runtime import Core
except Exception:
    Core = None


class InferenceRunner:
    def __init__(self, model_path, backend='onnxruntime', input_size=640, conf_thresh=0.3):
        self.model_path = model_path
        self.backend = backend
        self.input_size = input_size
        self.conf_thresh = conf_thresh
        self.session = None
        self.compiled_model = None
        if backend == 'onnxruntime':
            if ort is None:
                raise RuntimeError('onnxruntime is not installed')
            self.session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
        elif backend == 'openvino':
            if Core is None:
                raise RuntimeError('openvino.runtime not available')
            core = Core()
            model = core.read_model(model_path)
            self.compiled_model = core.compile_model(model, 'CPU')
        else:
            raise ValueError('Unsupported backend')

    def preprocess(self, frame):
        img = cv2.resize(frame, (self.input_size, self.input_size))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
        img = np.transpose(img, (2, 0, 1))[None, ...]
        return img

    def infer(self, frame):
        x = self.preprocess(frame)
        if self.backend == 'onnxruntime':
            inp_name = self.session.get_inputs()[0].name
            t0 = time.time()
            outs = self.session.run(None, {inp_name: x})
            latency = time.time() - t0
            return outs, latency
        else:
            input_name = self.compiled_model.inputs[0].get_any_name()
            t0 = time.time()
            res = self.compiled_model([x])[self.compiled_model.outputs[0]]
            latency = time.time() - t0
            return [res], latency


def postprocess_onnx_output(outs, conf_thresh, orig_w, orig_h):
    # This is model-dependent. For many YOLO exports, postprocessing required.
    # We assume outs[0] is (N, 6) or (num_dets, attributes) rows with [cx, cy, w, h, conf, class]
    detections = []
    arr = np.array(outs[0])
    if arr.ndim == 3:
        arr = arr[0]
    for row in arr:
        if len(row) < 6:
            continue
        conf = float(row[4])
        if conf < conf_thresh:
            continue
        cx, cy, bw, bh = float(row[0]), float(row[1]), float(row[2]), float(row[3])
        x1 = int((cx - bw/2) * orig_w)
        y1 = int((cy - bh/2) * orig_h)
        x2 = int((cx + bw/2) * orig_w)
        y2 = int((cy + bh/2) * orig_h)
        cls = int(row[5]) if len(row) > 5 else -1
        detections.append({'label_id': cls, 'conf': conf, 'bbox': [x1, y1, x2, y2]})
    return detections


def run_benchmark(args):
    os.makedirs(args.out_dir, exist_ok=True)
    cap = cv2.VideoCapture(int(args.source) if args.source.isdigit() else args.source)
    runner = InferenceRunner(args.model, backend=args.backend, input_size=args.img, conf_thresh=args.conf)

    csv_path = os.path.join(args.out_dir, 'benchmark_log.csv')
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['timestamp', 'frame_idx', 'latency_s', 'fps', 'cpu_percent', 'detections'])

        frame_idx = 0
        latencies = deque(maxlen=100)
        t0 = time.time()
        last_trigger = 0.0
        cooldown = args.cooldown

        while frame_idx < args.frames:
            ret, frame = cap.read()
            if not ret:
                break
            orig_h, orig_w = frame.shape[:2]
            start = time.time()
            try:
                outs, latency = runner.infer(frame)
            except Exception as e:
                logging.exception('Inference failed: %s', e)
                break
            latencies.append(latency)
            fps = 1.0 / (time.time() - t0) if frame_idx > 0 else 0.0
            t0 = time.time()
            cpu = psutil.cpu_percent(interval=None)
            detections = postprocess_onnx_output(outs, args.conf, orig_w, orig_h)
            # check for trigger
            triggered = False
            if len(detections) > 0:
                now = time.time()
                if now - last_trigger >= cooldown:
                    # save detection image
                    ts = datetime.utcnow().strftime('%Y%m%dT%H%M%S')
                    fname = os.path.join(args.out_dir, f'detection_{ts}_f{frame_idx}.jpg')
                    cv2.imwrite(fname, frame)
                    last_trigger = now
                    triggered = True

            writer.writerow([datetime.utcnow().isoformat(), frame_idx, latency, round(np.mean(latencies) if latencies else 0, 4), cpu, len(detections)])
            if args.verbose:
                logging.info('Frame %d latency=%.3fs cpu=%.1f detections=%d triggered=%s', frame_idx, latency, cpu, len(detections), triggered)
            frame_idx += 1

    cap.release()


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--model', required=True, help='Path to ONNX or OpenVINO model')
    p.add_argument('--backend', choices=['onnxruntime', 'openvino'], default='onnxruntime')
    p.add_argument('--source', default='0', help='Camera index or video file')
    p.add_argument('--frames', type=int, default=200)
    p.add_argument('--img', type=int, default=640)
    p.add_argument('--conf', type=float, default=0.3)
    p.add_argument('--cooldown', type=float, default=10.0, help='Seconds to wait between triggers')
    p.add_argument('--out-dir', default='detections', help='Directory to save detection images and logs')
    p.add_argument('--verbose', action='store_true')
    return p.parse_args()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    args = parse_args()
    run_benchmark(args)
