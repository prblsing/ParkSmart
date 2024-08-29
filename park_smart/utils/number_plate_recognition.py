import cv2
import pytesseract
import numpy as np


def identify_car_number(image, car_box):
    """
    Extracts and identifies the car number from the image section containing the car.

    Args:
        image (np.array): The image containing the car.
        car_box (tuple): A tuple containing the coordinates of the bounding box (x1, y1, x2, y2).

    Returns:
        str: The identified car number or "UNKNOWN" if not identified.
    """
    # Extract the region of interest (ROI) from the image using the bounding box
    x1, y1, x2, y2 = car_box
    car_roi = image[y1:y2, x1:x2]

    # Convert to grayscale
    gray = cv2.cvtColor(car_roi, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and improve OCR accuracy
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply edge detection to highlight text
    edges = cv2.Canny(blurred, 50, 150)

    # Apply thresholding to get a binary image (black and white)
    _, binary = cv2.threshold(edges, 150, 255, cv2.THRESH_BINARY)

    # Perform OCR using Tesseract
    car_number = pytesseract.image_to_string(binary,
                                             config='--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

    # Clean up the car number by removing any non-alphanumeric characters
    car_number = ''.join(filter(str.isalnum, car_number))

    # If OCR does not find any text, return "UNKNOWN"
    if not car_number:
        car_number = "UNKNOWN"

    return car_number
