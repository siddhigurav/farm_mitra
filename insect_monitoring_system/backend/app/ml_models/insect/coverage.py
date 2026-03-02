from ultralytics import YOLO
import numpy as np
import cv2

# Load a pretrained YOLOv8 segmentation model
model = YOLO('yolov8n-seg.pt') # Using a nano segmentation model

def calculate_area_coverage(image_path):
    """
    Calculates the percentage of an image covered by insect masks.
    """
    image = cv2.imread(image_path)
    if image is None:
        return {"error": "Image not found"}

    height, width, _ = image.shape
    total_area = height * width

    # Run inference
    results = model(image)

    # Process results
    total_mask_area = 0
    for result in results:
        if result.masks is not None:
            masks = result.masks.data.cpu().numpy()
            for mask in masks:
                total_mask_area += np.sum(mask)

    coverage_percentage = (total_mask_area / total_area) * 100 if total_area > 0 else 0

    return {"coverage_percentage": coverage_percentage}