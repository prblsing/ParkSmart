import streamlit as st
from park_smart.config.logging_config import get_logger
from park_smart.config.model_config import load_yolo_model
from park_smart.utils.parking_validations import draw_bounding_boxes, is_car_parked_correctly
from park_smart.utils.image_processing import preprocess_image, detect_cars, detect_parking_lines
from park_smart.utils.database import initialize_database, insert_record, fetch_records
from PIL import Image
import numpy as np
from datetime import datetime
import sqlite3
import os

# Initialize logger
logger = get_logger(__name__, log_level='INFO')

@st.cache_resource
def initialize_yolo_model():
    """Lazy loading of the YOLO model."""
    return load_yolo_model()

@st.cache_resource
def initialize_db():
    """Lazy loading of the database connection."""
    return initialize_database()

def main():
    st.title('ParkSmart Analytics')
    st.sidebar.header("Navigation")

    # User login and tabs
    tabs = st.sidebar.radio("Select a view", ["User Dashboard", "Admin Dashboard"])

    if tabs == "User Dashboard":
        user_dashboard()
    elif tabs == "Admin Dashboard":
        admin_dashboard()

def user_dashboard():
    st.header("Upload Parking Image")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Load image
        image = np.array(Image.open(uploaded_file))
    
        # Detect parking lines
        parking_lines_img, parking_spaces = detect_parking_lines(image.copy())
    
        # Detect cars
        car_boxes = detect_cars(image.copy())
    
        # Ensure parking lines and car boxes are correctly processed
        if parking_lines_img is not None and car_boxes is not None:
            # Draw bounding boxes
            image_with_boxes, analysis = draw_bounding_boxes(parking_lines_img.copy(), car_boxes, parking_spaces)
        
            # Display results
            st.image(image_with_boxes, caption="Processed Image with Detected Cars", use_column_width=True)
        
            if car_boxes:
                st.warning(f"Detected {len(car_boxes)} cars in the parking lot.")
            else:
                st.success("No cars detected in the parking lot.")
        else:
            st.error("Error processing image. Please check the uploaded image.")
    
def admin_dashboard():
    st.header("Admin Dashboard")
    username = st.text_input("Username", value="admin")
    password = st.text_input("Password", value="admin", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin":
            st.success("Logged in successfully!")
            # conn = initialize_db()  # Use cached database connection
            # records = fetch_records(conn)
            # for record in records:
            #     st.write(f"Record ID: {record[0]}, Car Number: {record[2]}, Status: {record[4]}")
            #     action = st.selectbox("Action", ["Issue First Warning", "Issue Second Warning", "Issue Third Warning",
            #                                      "Revoke Parking Sticker"], key=record[0])
            #     if st.button("Apply", key=f"apply_{record[0]}"):
            #         new_status = action
            #         cursor = conn.cursor()
            #         cursor.execute('UPDATE parking_records SET status=? WHERE id=?', (new_status, record[0]))
            #         conn.commit()
            #         st.write(f"Status updated to {new_status}")
        else:
            st.error("Invalid credentials.")

if __name__ == "__main__":
    main()
