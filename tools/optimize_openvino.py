"""
Optimize ONNX model to OpenVINO IR using Model Optimizer (if installed).

Usage:
    python optimize_openvino.py --onnx models/yolov8n.onnx --out models/openvino/

Requires OpenVINO's Model Optimizer installed and on PATH as `mo`.
"""
import argparse
import os
import subprocess
import logging


def optimize(onnx_path: str, output_dir: str, input_shape: str = "[1,3,640,640]"):
    os.makedirs(output_dir, exist_ok=True)
    cmd = [
        "mo",
        "--input_model", onnx_path,
        "--input_shape", input_shape,
        "--output_dir", output_dir,
        "--data_type", "FP16",
    ]
    logging.info("Running Model Optimizer: %s", " ".join(cmd))
    subprocess.check_call(cmd)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--onnx", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--shape", default="[1,3,640,640]")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    optimize(args.onnx, args.out, args.shape)


if __name__ == "__main__":
    main()
