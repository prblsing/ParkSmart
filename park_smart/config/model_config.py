# model_config.py
import os
import torch
import gdown
import streamlit as st

# Define the path for the YOLOv5 model
MODEL_DIR = 'models'
MODEL_PATH = os.path.join(MODEL_DIR, 'pretrained_model_state_dict.pt')

def download_model():
    """
    Downloads the YOLO model from a Google Drive URL if not already present.
    """
    drive_url = os.getenv('DRIVE_URL')
    model_path = os.path.join('models', 'pretrained_model_state_dict.pt')
    
    if not os.path.exists('models'):
        os.makedirs('models')

    if not os.path.exists(model_path):
        try:
            gdown.download(drive_url, model_path, quiet=False)
        except Exception as e:
            logging.error(f"Failed to download the model: {e}")
            raise

def load_yolo_model():
    """
    Loads the YOLOv5 model after downloading it if necessary.
    """
    download_model()

    if os.path.exists(MODEL_PATH):
        # Load the model's state dict
        model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        model.load_state_dict(torch.load(MODEL_PATH))
        model.eval()  # Set the model to evaluation mode
        return model
    else:
        st.error("Model file does not exist. Please check the model download process.")
        return None
