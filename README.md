# ParkSmart Analytics

A research project using computer vision to detect parking violations from parking lot images. Built with Streamlit and Python, it identifies improperly parked cars, logs violations, and provides a dashboard for review and management. Ideal for exploring AI in everyday scenarios.

## Overview

Parking management can be challenging, especially in busy areas where improper parking can lead to reduced capacity and congestion. ParkSmart Analytics aims to provide a simple tool to analyze parking lot images, detect improperly parked cars, and log these incidents for review.

This project is purely for R&D purposes and aims to explore the capabilities of image analysis and machine learning in addressing everyday problems like parking management.

## Features

- **Parking Violation Detection:** Identifies cars that are not parked correctly within the designated parking lines.
- **Image Analysis:** Uses computer vision models such as YOLOv5 to detect cars and parking lines.
- **Logging and Record-Keeping:** Stores records of violations, including images and status updates.
- **User Dashboard:** Allows users to upload images and view past violation records.
- **Admin Dashboard:** Provides basic admin controls to manage parking violations (issue warnings, etc.).

## Project Structure

```
parking_violation_detection/
│
├── park_smart/                     
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── logging_config.py       
│   │   ├── model_config.py         
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── image_processing.py             
│   │   ├── database.py             
│   │   ├── number_plate_recognition.py 
│   │   ├── parking_validations.py  
├── app.py                          
├── requirements.txt                
└── data/                           
    └── park_smart.db
```

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Streamlit
- OpenCV
- NumPy
- Pillow
- PyTorch

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/parking_violation_detection.git
   cd parking_violation_detection
   ```

2. **Install Dependencies**

   Use pip to install the necessary packages:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**

   Start the Streamlit app:

   ```bash
   streamlit run app.py
   ```

4. **Open in Browser**

   Visit `http://localhost:8501` to access the app.

## Usage

- **User Dashboard:** Upload an image to analyze for parking violations or view past violation records.
- **Admin Dashboard:** Log in as an admin to manage violations (issue warnings, etc.).

## Future Work

- **Enhance Car Detection Accuracy:** Improve detection accuracy by refining models and training data.
- **License Plate Recognition:** Add functionality for license plate recognition.
- **Advanced Analytics:** Incorporate more detailed parking analytics, such as space utilization rates.

## Contributions and License

This project is licensed under the MIT License. Contributions, suggestions, and collaboration are welcomed! Feel free to fork the repository and submit a pull request.

## Disclaimer

This project is intended for educational and research purposes only.
