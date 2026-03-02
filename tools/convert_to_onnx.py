"""
Export YOLOv8 model to ONNX using ultralytics (recommended on workstation).

Usage:
    python convert_to_onnx.py --weights yolov8n.pt --out models/yolov8n.onnx --img 640

Notes:
- This script requires the `ultralytics` package installed on a machine with PyTorch.
- Exporting on-device (Raspberry Pi) is slow; prefer exporting on a desktop and copy ONNX to Pi.
"""
import argparse
import os
import logging

def export_to_onnx(weights: str, out: str, img_size: int = 640, opset: int = 12):
    try:
        from ultralytics import YOLO
    except Exception as e:
        raise RuntimeError("ultralytics not installed or cannot be imported") from e

    model = YOLO(weights)
    # export to onnx; ultralytics export method supports onnx
    logging.info("Exporting %s -> %s (img=%d,opset=%d)", weights, out, img_size, opset)
    # ultralytics YOLO.export supports args like format='onnx'
    model.export(format='onnx', imgsz=img_size, opset=opset, simplify=True, dynamic=True, save=True)
    # the exported file name is usually in runs/ or models/, try to move
    # if out path is provided and exists, do nothing; otherwise try to find and move
    if os.path.exists(out):
        logging.info("ONNX exported to %s", out)
    else:
        logging.warning("Requested out path %s does not exist; check ultralytics export output", out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--weights", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--img", type=int, default=640)
    parser.add_argument("--opset", type=int, default=12)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    export_to_onnx(args.weights, args.out, args.img, args.opset)


if __name__ == "__main__":
    main()
