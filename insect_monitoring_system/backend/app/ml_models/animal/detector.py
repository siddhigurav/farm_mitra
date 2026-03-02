from ultralytics import YOLO
import cv2

# Load a pretrained YOLOv8 model for animal detection
model = YOLO('yolov8n.pt') # Using a general model, can be fine-tuned

def detect_animals_from_image(image_path):
    """
    Detects animals in an image using a YOLOv8 model.
    """
    image = cv2.imread(image_path)
    if image is None:
        return {"error": "Image not found"}

    # Run inference
    results = model(image)

    # Process results for animal classes
    detections = []
    animal_classes = ['bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe'] # Example classes
    for result in results:
        boxes = result.boxes
        for box in boxes:
            cls = int(box.cls[0].item())
            class_name = model.names[cls]
            if class_name in animal_classes:
                detections.append({
                    "box": box.xyxy[0].tolist(),
                    "confidence": box.conf[0].item(),
                    "class_name": class_name
                })

    return {"detections": detections}