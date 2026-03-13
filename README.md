# Smart Hotel Monitoring System

An automated surveillance solution designed for smart hotels to monitor kitchen environments in real-time. This system uses **YOLOv8** computer vision to detect hygiene violations (missing aprons, gloves, or hairnets) and pest activity (cockroaches, lizards, or rats).

## 🚀 Key Features

* **Real-time AI Detection**: Leverages YOLOv8 to identify specific hygiene and pest violations from live camera feeds.
* **Automated Email Alerts**: Instantly notifies management via email with attached snapshots when a violation is detected.
* **Interactive Dashboard**: A modern web interface featuring live video streaming, real-time violation logs, and statistical breakdowns.
* **Smart Cooldown Logic**: Prevents notification spam by enforcing a 30-second cooldown period between repeated alerts for the same violation type.
* **Log Management**: Dynamically updated logs with filtering capabilities for pests versus hygiene issues.

## 🛠️ Tech Stack

* **Backend**: FastAPI
* **AI Model**: Ultralytics YOLOv8
* **Computer Vision**: OpenCV
* **Frontend**: HTML5, CSS3 (Inter font), and  JavaScript
* **Communication**: SMTP for email notifications

## 📂 Project Structure

* `main.py`: The core FastAPI application handling model inference, email logic, and API endpoints.
* `templates/index.html`: The web dashboard for monitoring the system.
* `best.pt`: The trained YOLOv8 model weights.
* `snapshots/`: Directory where violation evidence images are automatically stored.
* `demo2.mp4`: Sample video file used for demonstration purposes.

## 🔧 Setup Instructions

### 1. Prerequisites

Ensure you have Python 3.11+ installed.

### 2. Installation

```bash
pip install fastapi ultralytics opencv-python uvicorn jinja2

```

### 3. Email Configuration

Update the following variables in `main.py` with your credentials:

* `SENDER_EMAIL`: Your Gmail address.
* `APP_PASSWORD`: Your Google App Password (not your standard password).
* `RECEIVER_EMAIL`: The recipient's email address.

### 4. Running the Application

Navigate to the project directory and run:

```bash
uvicorn main:app --reload

```

Access the dashboard at `http://127.0.0.1:8000`.

## 🚨 Monitored Violations

* **Pests**: Cockroaches, Lizards, Rats.
* **Hygiene**: No Apron, No Gloves, No Hairnet.

## 📝 License

This project was developed for technical hackathon purposes and smart hotel kitchen safety monitoring.
