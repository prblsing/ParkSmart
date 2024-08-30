import streamlit as st
from park_smart.config.logging_config import get_logger
from park_smart.config.model_config import load_yolo_model
from park_smart.utils.parking_validations import draw_bounding_boxes, is_car_parked_correctly
from park_smart.utils.image_processing import preprocess_image, detect_cars, detect_parking_lines
from park_smart.utils.database import initialize_database, insert_record, fetch_records
from park_smart.utils.number_plate_recognition import identify_car_number
from PIL import Image
import numpy as np
from datetime import datetime


# Initialize the model
yolo_model = load_yolo_model()

# Initialize logger
logger = get_logger(__name__, log_level='INFO')

# Load models
yolo_model = load_yolo_model()

# Initialize database
conn = initialize_database()

# Streamlit app
st.title('ParkSmart Analytics')
st.sidebar.header("Navigation")

# User login and tabs
tabs = st.sidebar.radio("Select a view", ["User Dashboard", "Admin Dashboard"])

if tabs == "User Dashboard":
    st.header("Upload Parking Image")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = np.array(Image.open(uploaded_file))
        image_with_lines, parking_spaces = detect_parking_lines(image.copy())
        car_boxes = detect_cars(image)
        final_image, analysis = draw_bounding_boxes(image_with_lines, car_boxes, parking_spaces)

        st.image(final_image, caption="Processed Image with Detected Cars", use_column_width=True)
        st.write(f"Detected {len(car_boxes)} cars in the parking lot.")

        for item in analysis:
            if "Incorrectly" in item:
                car_number = identify_car_number(final_image, car_boxes[analysis.index(item)])
                report_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                insert_record(conn, uploaded_file.name, car_number, report_date, "Pending")
                st.error(item)
            else:
                st.success(item)

elif tabs == "Admin Dashboard":
    st.header("Admin Dashboard")
    username = st.text_input("Username", value="admin")
    password = st.text_input("Password", value="admin", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin":
            st.success("Logged in successfully!")
            records = fetch_records(conn)
            for record in records:
                st.write(f"Record ID: {record[0]}, Car Number: {record[2]}, Status: {record[4]}")
                action = st.selectbox("Action", ["Issue First Warning", "Issue Second Warning", "Issue Third Warning",
                                                 "Revoke Parking Sticker"], key=record[0])
                if st.button("Apply", key=f"apply_{record[0]}"):
                    new_status = action
                    cursor = conn.cursor()
                    cursor.execute('UPDATE parking_records SET status=? WHERE id=?', (new_status, record[0]))
                    conn.commit()
                    st.write(f"Status updated to {new_status}")
        else:
            st.error("Invalid credentials.")
