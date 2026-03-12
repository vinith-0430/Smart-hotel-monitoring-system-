from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from ultralytics import YOLO
import cv2
from datetime import datetime
import smtplib
from email.message import EmailMessage
import threading
import time
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Create a folder to save snapshot images for emails
os.makedirs("snapshots", exist_ok=True)

# Load YOLO model
model = YOLO("best.pt")
video_path = "demo.mp4"
cap = cv2.VideoCapture(video_path)

# Classes considered violations
violations = ["cockroach", "lizard", "rat", "no_apron", "no_gloves", "no_hairnet"]

# Keep logs of violations
violation_logs = []

# --- EMAIL CONFIGURATION ---
SENDER_EMAIL = "vinithmohan2006@gmail.com"  # Replace with your email
APP_PASSWORD = "bxli unmn pwbv abol" # Replace with your App Password
RECEIVER_EMAIL = "vinithmohan2006@gmail.com" # Replace with the owner's email

# --- COOLDOWN LOGIC ---
COOLDOWN_SECONDS = 30  # Wait 30 seconds before sending another email for the same violation
last_email_sent_time = {}

def send_alert_email(label, timestamp, image_path):
    """Sends an email with the violation details and snapshot attachment."""
    try:
        msg = EmailMessage()
        msg['Subject'] = f"⚠️ Kitchen Violation Alert: {label.upper()}"
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        
        msg.set_content(f"A hygiene/pest violation was detected in the kitchen.\n\n"
                        f"Violation: {label}\n"
                        f"Time: {timestamp}\n\n"
                        f"Please see the attached snapshot for evidence.")

        # Attach the image
        with open(image_path, 'rb') as f:
            img_data = f.read()
        msg.add_attachment(img_data, maintype='image', subtype='jpeg', filename=f"{label}_{timestamp.replace(':', '-')}.jpg")

        # Send the email via Gmail SMTP
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)
            
        print(f"[{timestamp}] ✅ Alert email sent for {label}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def generate_frames():
    global violation_logs, last_email_sent_time
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            # Optional: Loop video if it ends
            # cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            break

        results = model(frame, verbose=False)
        annotated_frame = results[0].plot()  # Bounding boxes only

        # Check for violations
        current_time = time.time()
        for box in results[0].boxes:
            class_id = int(box.cls)
            label = model.names[class_id]

            if label in violations:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Check cooldown to prevent email spam
                if label not in last_email_sent_time or (current_time - last_email_sent_time[label]) > COOLDOWN_SECONDS:
                    
                    # Update cooldown timer
                    last_email_sent_time[label] = current_time
                    
                    # Append to logs
                    violation_logs.append({"timestamp": timestamp, "label": label})
                    print(f"[{timestamp}] 🚨 Violation detected: {label}")
                    
                    # Save a snapshot of the frame to attach to the email
                    safe_timestamp = timestamp.replace(":", "-")
                    snapshot_path = f"snapshots/{label}_{safe_timestamp}.jpg"
                    cv2.imwrite(snapshot_path, annotated_frame)
                    
                    # Spawn a new thread to send the email so the video stream doesn't freeze
                    threading.Thread(target=send_alert_email, args=(label, timestamp, snapshot_path), daemon=True).start()

        # Encode frame for streaming
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# Routes
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/video_feed")
def video_feed():
    return StreamingResponse(generate_frames(),
                             media_type='multipart/x-mixed-replace; boundary=frame')

@app.get("/logs")
def get_logs():
    return JSONResponse(content=violation_logs)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)