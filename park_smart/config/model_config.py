# model_config.py
import torch
import os
import gdown

# Path to the YOLOv5 model file
MODEL_PATH = 'models/pretrained_model_state_dict.pt'
DRIVE_URL = 'https://drive.google.com/uc?id=1zWhDEF8WkDDRrrGeu23ySXWAYi1QKWfg'


def download_model():
    """
    Downloads the YOLOv5 model from Google Drive if it does not exist.
    """
    if not os.path.exists(MODEL_PATH):
        # Ensure the models directory exists
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

        # Download model from Google Drive
        print(f"Downloading YOLOv5 model to {MODEL_PATH}...")
        gdown.download(DRIVE_URL, MODEL_PATH, quiet=False)
    else:
        print(f"Model already exists at {MODEL_PATH}.")


def load_yolo_model():
    """
    Loads the YOLOv5 model after downloading if necessary.
    """
    download_model()

    # Load the model's state dict
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    model.load_state_dict(torch.load(MODEL_PATH))
    model.eval()  # Set the model to evaluation mode
    return model
