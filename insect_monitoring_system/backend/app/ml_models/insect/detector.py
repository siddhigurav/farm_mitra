from ultralytics import YOLO
import cv2

# Load a pretrained YOLOv8 model
model = YOLO('yolov8n.pt') # Using a nano model as an example

# Define harmful insects for grapes and guava
GRAPE_HARMFUL_INSECTS = [
    'grape_berry_moth', 'grape_leafhopper', 'grape_phylloxera', 
    'grape_root_borer', 'grape_cane_girdler'
]

GUAVA_HARMFUL_INSECTS = [
    'fruit_borer', 'mealybug', 'aphid', 
    'scale_insect', 'thrips'
]

# Define useful insects (beneficial for crops)
USEFUL_INSECTS = [
    'bee', 'ladybug', 'lacewing', 
    'parasitic_wasp', 'spider'
]

def detect_insects_from_image(image_path, crop_type="general"):
    """
    Detects insects in an image using a YOLOv8 model.
    Includes classification of harmful vs useful insects for grapes and guava.
    """
    image = cv2.imread(image_path)
    if image is None:
        return {"error": "Image not found"}

    # Run inference on the image
    results = model(image)

    # Process results
    detections = []
    for result in results:
        boxes = result.boxes
        for box in boxes:
            xyxy = box.xyxy[0].tolist()
            conf = box.conf[0].item()
            cls = int(box.cls[0].item())
            class_name = model.names[cls]
            
            # Determine if insect is harmful or useful based on crop type
            is_harmful = True
            recommended_action = "Monitor"
            
            if class_name in USEFUL_INSECTS:
                is_harmful = False
                recommended_action = "Protect beneficial insect"
            elif crop_type.lower() == "grapes" and class_name in GRAPE_HARMFUL_INSECTS:
                recommended_action = "Apply targeted pesticide treatment"
            elif crop_type.lower() == "guava" and class_name in GUAVA_HARMFUL_INSECTS:
                recommended_action = "Apply targeted pesticide treatment"
            elif class_name in GRAPE_HARMFUL_INSECTS or class_name in GUAVA_HARMFUL_INSECTS:
                recommended_action = "Monitor closely and consider treatment"
            
            detections.append({
                "box": xyxy,
                "confidence": conf,
                "class_name": class_name,
                "is_harmful": is_harmful,
                "recommended_action": recommended_action,
                "crop_type": crop_type
            })

    return {"detections": detections}