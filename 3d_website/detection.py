import PIL
from ultralytics import YOLO
import torch
from ultralytics.nn.tasks import DetectionModel
from torch.nn.modules.container import Sequential

def detect_doors(image, confidence=0.4):
    """
    Detect doors in the uploaded image using YOLOv8.
    Returns list of door bounding boxes: [{'x': x, 'y': y, 'w': w, 'h': h}, ...]
    """
    torch.serialization.add_safe_globals([DetectionModel, Sequential])
    model = YOLO('../best.pt')  # Assuming best.pt is in parent dir

    res = model.predict(image, conf=confidence)
    # Filter only doors
    door_boxes = [box for box in res[0].boxes if model.names[int(box.cls)] == 'Door']

    doors = []
    for box in door_boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        w = x2 - x1
        h = y2 - y1
        doors.append({'x': x1 + w/2, 'y': y1 + h/2, 'w': w, 'h': h})  # Center and size

    return doors
