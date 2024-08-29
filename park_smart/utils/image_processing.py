import cv2
import numpy as np
from park_smart.config.logging_config import get_logger
from park_smart.config.model_config import load_yolo_model

logger = get_logger(__name__, log_level='INFO')
yolo_model = load_yolo_model()


def preprocess_image(image):
    """
    Preprocess the image for edge detection.

    Args:
        image (np.array): Input image array.

    Returns:
        np.array: Edge-detected image.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    return edges


def detect_parking_lines(image):
    logger.info("Detecting parking lines in the image.")
    edges = preprocess_image(image)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)
    parking_spaces = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            parking_spaces.append([(x1, y1), (x2, y2)])  # Store as a list of points
        logger.info(f"Detected {len(lines)} parking lines.")
    else:
        logger.warning("No parking lines detected.")
    return image, parking_spaces


def detect_cars(image):
    logger.info("Detecting cars using YOLOv5 model.")
    results = yolo_model(image)
    car_boxes = []
    for *box, conf, cls in results.xyxy[0].numpy():
        if int(cls) == 2 and conf > 0.5:  # Class 2 is 'car' in COCO dataset
            car_boxes.append(list(map(int, box)))
    logger.info(f"Detected {len(car_boxes)} cars.")
    return car_boxes
