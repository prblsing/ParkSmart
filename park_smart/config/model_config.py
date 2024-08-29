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
    Downloads the YOLOv5 model from Google Drive if it does not exist.
    """
    if not os.path.exists(MODEL_PATH):
        # Ensure the models directory exists
        os.makedirs(MODEL_DIR, exist_ok=True)

        # Get the Google Drive URL from Streamlit secrets
        drive_url = st.secrets.get("DRIVE_URL", None)
        if drive_url:
            print(f"Downloading YOLOv5 model from {drive_url} to {MODEL_PATH}...")
            gdown.download(drive_url, MODEL_PATH, quiet=False)
        else:
            st.error("Drive URL is not set in Streamlit secrets.")
    else:
        print(f"Model already exists at {MODEL_PATH}.")

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
