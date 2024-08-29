import cv2
import numpy as np
from park_smart.config.logging_config import get_logger

logger = get_logger(__name__, log_level='INFO')


def is_car_parked_correctly(car_box, parking_spaces, image):
    # Focus on car's contour rather than the bounding box for more precise checking
    car_image = image[car_box[1]:car_box[3], car_box[0]:car_box[2]]
    car_gray = cv2.cvtColor(car_image, cv2.COLOR_BGR2GRAY)
    _, car_thresh = cv2.threshold(car_gray, 128, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(car_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        logger.warning("No contours found for the car.")
        return False

    # Approximate car contour
    car_contour = max(contours, key=cv2.contourArea)
    car_hull = cv2.convexHull(car_contour)

    for line in parking_spaces:
        p1, p2 = line  # Unpack line points
        # Convert points to tuple format
        p1 = (int(p1[0]), int(p1[1]))
        p2 = (int(p2[0]), int(p2[1]))

        # Check if any of the parking line points are within the car's contour
        if cv2.pointPolygonTest(car_hull, p1, False) >= 0 or cv2.pointPolygonTest(car_hull, p2, False) >= 0:
            return False

    return True


def draw_bounding_boxes(image, car_boxes, parking_spaces):
    """
    Draw bounding boxes around detected cars and annotate them.

    Args:
        image (np.array): Original image array.
        car_boxes (list): List of bounding boxes for detected cars.
        parking_spaces (list): List of parking space coordinates.
        logger (logger.Logger): Logger instance for logger.

    Returns:
        np.array, list: Annotated image, list of car parking analysis.
    """
    analysis = []

    # Convert the original image to RGBA
    output_image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

    # Create an overlay in RGBA format
    overlay = np.zeros_like(output_image, dtype=np.uint8)

    for i, box in enumerate(car_boxes):
        is_correct = is_car_parked_correctly(box, parking_spaces, image)
        color = (0, 255, 0, 128) if is_correct else (0, 0, 255, 128)  # RGBA format with transparency
        darker_green = (0, 100, 0, 255)
        darker_red = (100, 0, 0, 255)
        color_circle = darker_green if is_correct else darker_red

        logger.info(f"Drawing rectangle with color: {color}")

        # Draw the bounding box on the overlay
        cv2.rectangle(overlay, (box[0], box[1]), (box[2], box[3]), color, 2)

        # Draw car number with a dark background (black circle) and white text
        text = str(i + 1)
        font_scale = 0.6
        thickness = 1
        text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
        text_w, text_h = text_size

        circle_center = (box[0] + 20, box[1] - 20)
        circle_radius = max(text_w, text_h) // 2 + 10

        # Draw filled circle in black with some transparency
        cv2.circle(overlay, circle_center, circle_radius, color_circle, -1)
        text_x = circle_center[0] - text_w // 2
        text_y = circle_center[1] + text_h // 2

        # Put the text in white on top of the circle
        cv2.putText(overlay, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255, 255),
                    thickness, cv2.LINE_AA)

        logger.info(f"Number {i + 1} drawn at: {circle_center} with text position: ({text_x}, {text_y})")

        status = "Correctly" if is_correct else "Incorrectly"
        analysis.append(f"Car {i + 1}: {status} parked")
        logger.info(f"Car {i + 1} is {status} parked.")

    # Combine the overlay with the original image using alpha blending
    cv2.addWeighted(overlay, 1, output_image, 1, 0, output_image)

    return output_image, analysis
