# Topic: Face Recognition System - Part 3: Real-time Recognition

import cv2
import csv
import os
import pygame
import threading
import time
from twilio.rest import Client
import smtplib
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv
# === Load environment variables ===
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
ENV_PATH = os.path.join(PROJECT_ROOT, '.env')
load_dotenv(dotenv_path=ENV_PATH)
# === Setup Directories ===
# CHANGED: CAPTURED_IMAGES_DIR now points to the subfolder 'Terrorist_Data'
CAPTURED_IMAGES_DIR = os.path.join(PROJECT_ROOT, 'static', 'captured_faces', 'Terrorist_Data')
DETECTION_LOG_PATH = os.path.join(PROJECT_ROOT, 'data', 'detection_log.csv')
PATH_TO_TRAINER = os.path.join(PROJECT_ROOT, 'data','trainer.yml')
HAARCASCADE_PATH = os.path.join(PROJECT_ROOT, 'static', 'haarcascade_frontalface_default.xml')
AUDIO_PATH = os.path.join(PROJECT_ROOT, 'static','alarm.wav')
# === Load environment variables ===
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

# === Setup Directories ===
if not os.path.exists(CAPTURED_IMAGES_DIR):
    os.makedirs(CAPTURED_IMAGES_DIR)
    print("[INFO] Created Terrorist_Data directory.")

# === Load Recognizer and Haar Cascade ===
recognizer = cv2.face.LBPHFaceRecognizer_create()
try:
    recognizer.read(PATH_TO_TRAINER)
    print("[INFO] Loaded trainer.yml successfully.")
except cv2.error as e:
    print(f"[ERROR] Failed to load trainer.yml: {e}")
    exit()

faceCascade = cv2.CascadeClassifier(HAARCASCADE_PATH)
if faceCascade.empty():
    print("[ERROR] Failed to load haarcascade_frontalface_default.xml")
    exit()
font = cv2.FONT_HERSHEY_SIMPLEX

# === ID to Name Mapping ===
names = ['None', 'Kabil', 'ID2']
shown_ids = set()
notified_ids = set()

# === Person Details ===
person_details = {
    1: {
        "name": "Kabil",
        "Category": "Terrorist",
        "Nationality": "Unknown",
        "Crimes": ["Bombing", "Arms smuggling"],
        "Last Seen": "Chennai Central Station, May 2025",
        "Status": "Highly Dangerous"
    },
    2: {
        "name": "ID2",
        "Category": "Civilian",
        "Nationality": "Indian",
        "Occupation": "Software Engineer",
        "Last Seen": "Office, Chennai",
        "Status": "No Criminal Record"
    }
}

# === Alarm Sound ===
def play_alarm():
    def alarm_thread():
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(AUDIO_PATH)
            pygame.mixer.music.play()
            time.sleep(5)
            pygame.mixer.music.stop()
        except Exception as e:
            print(f"[ERROR] Alarm failed: {e}")
    threading.Thread(target=alarm_thread, daemon=True).start()

# === Email Alert ===
def send_email_with_image(image_path, id):
    sender_email = "bagyalakshmiselvasekar@gmail.com"
    sender_password = os.getenv('EMAIL_PASSWORD')
    receiver_email = "kabilanselvasekar@gmail.com"

    if not sender_password:
        print("[ERROR] EMAIL_PASSWORD not set.")
        return

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S IST")
    details = person_details.get(id, {})
    body = f"""
    <html>
      <body>
        <p>Dear Sir/Madam,</p>
        <p>This is an automated alert from the AI CCTV Security System.</p>
        <h3>Incident Report:</h3>
        <ul>
          <li><b>Name:</b> {details.get('name')}</li>
          <li><b>Category:</b> {details.get('Category')}</li>
          <li><b>Nationality:</b> {details.get('Nationality')}</li>
          <li><b>Crimes:</b> {', '.join(details.get('Crimes', []))}</li>
          <li><b>Last Seen:</b> {details.get('Last Seen')}</li>
          <li><b>Status:</b> {details.get('Status')}</li>
          <li><b>Detected At:</b> {timestamp}</li>
        </ul>
        <p>Please check attached image and take appropriate action.</p>
      </body>
    </html>
    """

    msg = EmailMessage()
    msg['Subject'] = "🚨 Alert: Terrorist Detected"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.add_alternative(body, subtype='html')

    with open(image_path, 'rb') as f:
        msg.add_attachment(f.read(), maintype='image', subtype='jpeg', filename=os.path.basename(image_path))

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        print("[INFO] Email sent.")
    except Exception as e:
        print(f"[ERROR] Email failed: {e}")

# === SMS Alert ===
_last_sms_time = 0
_sms_cooldown_seconds = 60

def send_sms_alert(id):
    global _last_sms_time
    now = time.time()
    if now - _last_sms_time < _sms_cooldown_seconds:
        return

    account_sid = os.getenv('TWILIO_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    from_number = os.getenv('TWILIO_PHONE_NUMBER')
    to_number = '+917299329846'

    if None in (account_sid, auth_token, from_number):
        print("[ERROR] Twilio credentials missing.")
        return

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S IST")
    details = person_details.get(id, {})
    message_text = f"🚨 ALERT: {details.get('name')} ({details.get('Category')}) detected. Last Seen: {details.get('Last Seen')}. Time: {timestamp}"

    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(body=message_text, from_=from_number, to=to_number)
        print(f"[INFO] SMS sent. SID: {message.sid}")
        _last_sms_time = now
    except Exception as e:
        print(f"[ERROR] SMS failed: {e}")

def log_detection_to_csv(id, category, filename):
    # Ensure filename is relative to static folder (for dashboard.html to use url_for)
    relative_path = os.path.join('captured_faces', 'Terrorist_Data', filename).replace('\\', '/')

    with open(DETECTION_LOG_PATH, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), id, id, category, relative_path])
        
# === Start Video Capture (Optimized) ===
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Warm-up camera
for _ in range(10):
    ret, _ = cap.read()

if not cap.isOpened():
    print("[ERROR] Could not open video capture.")
    exit()

print("[INFO] Video capture initialized.")
minW = 0.1 * cap.get(3)
minH = 0.1 * cap.get(4)

frame_count = 0
while True:
    frame_count += 1
    ret, img = cap.read()
    if not ret:
        break

    if frame_count % 2 != 0:
        continue

    img = cv2.flip(img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.2, 5, minSize=(int(minW), int(minH)))

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 165, 255), 2)
        id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
        conf = round(100 - confidence)  # Higher conf = better match

        # Set threshold for valid recognition
        CONFIDENCE_THRESHOLD = 30

        if conf > CONFIDENCE_THRESHOLD:
            # Only proceed if match is confident
            details = person_details.get(id, {})
            img_text = names[id] if id < len(names) else "Unknown"
            confidence_text = f"{conf}%"

            if id not in shown_ids:
                print("\n--- MATCHED INDIVIDUAL ---")
                for key, value in details.items():
                    print(f"{key}: {', '.join(value) if isinstance(value, list) else value}")
                shown_ids.add(id)

            # Display overlay
            y_offset = y + h + 25
            for key, value in details.items():
                text = f"{key}: {', '.join(value) if isinstance(value, list) else value}"
                cv2.putText(img, text, (x, y_offset), font, 0.5, (0, 255, 0), 1)
                y_offset += 20

            # Check terrorist category
            if details.get("Category", "").lower() == "terrorist":
                img_text += " [TERRORIST]"

                if id not in notified_ids:
                    timestamp = time.strftime("%Y%m%d-%H%M%S")
                    filename_only = f"auto_capture_{timestamp}.jpg"
                    full_path = os.path.join(CAPTURED_IMAGES_DIR, filename_only)
                    cv2.imwrite(full_path, img)
                    log_detection_to_csv(id, details.get("Category", ""), filename_only)

                    play_alarm()
                    threading.Thread(target=send_email_with_image, args=(full_path, id), daemon=True).start()
                    threading.Thread(target=send_sms_alert, args=(id,), daemon=True).start()

                    notified_ids.add(id)
            else:
                img_text = "Civilian"
                confidence_text = f"{conf}%"

            cv2.putText(img, img_text, (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, confidence_text, (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        else:
            # Low confidence — treat as unknown
            img_text = "Unknown"
            confidence_text = f"{conf}%"
            cv2.putText(img, img_text, (x + 5, y - 5), font, 1, (0, 0, 255), 2)
            cv2.putText(img, confidence_text, (x + 5, y + h - 5), font, 1, (0, 0, 255), 1)

    time.sleep(0.01)
    cv2.imshow('Face Recognition - Press ESC or C', img)
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break
    elif key == ord('c'):
        print('[INFO] Manual capture saved')
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"manual_capture_{timestamp}.jpg"
        filepath = os.path.join(CAPTURED_IMAGES_DIR, filename)
        # Use details from the last detected face if available, else fallback
        last_details = details if 'details' in locals() else {}
        log_category = last_details.get("Category", "")
        cv2.imwrite(filepath, img)
        log_detection_to_csv(id, log_category, filename)

# === Cleanup ===
print("[INFO] Exiting...")
cap.release()
cv2.destroyAllWindows()