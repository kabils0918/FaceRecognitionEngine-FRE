# AI CCTV Security System with Face Recognition & Alerting

## 📅 Project Overview

This project implements a real-time face recognition surveillance system designed to identify individuals categorized as "terrorists." Upon detection, the system triggers multiple alerts including audio, email, and SMS, and logs all events to a dashboard with visual reports.

## 🔧 Features

* **Real-time Face Detection:** Uses Haar Cascades to detect faces in live webcam streams.
* **Face Recognition:** Employs the LBPH algorithm for efficient and reliable face matching.
* **Dataset Creation & Training:**

  * Collect face datasets via a script.
  * Train a face recognition model using LBPH.
* **Alerting Mechanism:**

  * 📹 Visual on-screen alerts
  * 🎧 Audio alarm (`alarm.wav`)
  * 📧 Email notification with image
  * 📲 SMS alert via Twilio
* **Flask Web Dashboard:**

  * Displays the latest detection with image and details
  * Shows detection history in a searchable table
  * Downloadable CSV log
  * Interactive detection trend graph (via Chart.js)
  * Clear latest or all logs/images

## 📊 Technologies Used

* Python 3.x
* OpenCV, Pillow (PIL), NumPy
* Flask, Chart.js
* pygame
* smtplib (email)
* Twilio
* python-dotenv

## 📚 Directory Structure

```
.
├── app.py                        # Main Flask app
├── data/
│   ├── detection_log.csv         # Logs of all detections
│   ├── Face_datasets/           # Raw captured face images
│   └── trainer/trainer.yml      # Trained LBPH model
├── src/
│   ├── 01_Face_Dataset.py       # Collects face datasets
│   ├── 02_Face_Training.py      # Trains face recognition model
│   └── 03_Face_Recognition.py   # Runs detection + alerts
├── static/
│   ├── alarm.wav                # Audio alarm file
│   ├── haarcascade_frontalface_default.xml
│   └── captured_faces/Terrorist_Data/  # Detected face images
├── templates/
│   └── dashboard.html           # Dashboard HTML template
├── .env                         # API/email credentials
├── requirements.txt             # Python dependencies
├── run_project.bat              # Script to launch full system (Windows)
└── .gitignore                   # Files to ignore
```

## ✨ Getting Started

### ✅ Prerequisites

* Python 3.x
* Git
* Webcam
* Internet connection (for alerts)

### ① Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### ② Create & Activate Virtual Environment

```bash
python -m venv env_temp
# Windows:
./env_temp/Scripts/activate
# macOS/Linux:
source env_temp/bin/activate
```

### ③ Install Dependencies

```bash
pip install -r requirements.txt
```

### ④ Setup .env File

Create a `.env` file:

```env
EMAIL_PASSWORD="your_gmail_app_password"
TWILIO_SID="your_twilio_sid"
TWILIO_AUTH_TOKEN="your_twilio_auth_token"
TWILIO_PHONE_NUMBER="+1234567890"
```

### ⑤ Ensure Assets Are Present

Make sure the following files exist:

* `static/alarm.wav`
* `static/haarcascade_frontalface_default.xml`

---

## 🚀 Usage

### 1. Collect Face Dataset

```bash
python src/01_Face_Dataset.py
```

Enter a unique numeric ID when prompted. 30 face images will be saved to `data/Face_datasets/`.

### 2. Train the Model

```bash
python src/02_Face_Training.py
```

Trained model will be saved to `data/trainer/trainer.yml`.

### 3. Start the System

**Option 1:** Using `run_project.bat` (Windows only):

```bash
run_project.bat
```

**Option 2:** Manual launch:

```bash
# Terminal 1:
python src/03_Face_Recognition.py
# Terminal 2:
python app.py
```

### 4. Open the Dashboard

Visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📊 Dashboard Highlights

* **Latest Detection:** Info + image
* **Detection Table:** Searchable/filterable table
* **Trend Graph:** Daily detection count
* **Download Log:** Save CSV file
* **Clear Logs:** Delete latest or all entries/images

## ⚠️ Alerts Triggered by "Terrorist" Detection

* 🎧 Plays alarm sound
* 📧 Sends email alert with image
* 📲 Sends SMS alert via Twilio
* 📅 Logs the event + stores image in `static/captured_faces/Terrorist_Data/`

---

## 📝 Contributing

* Fork this repository
* Open issues / suggestions
* Submit pull requests

## ✉️ License

This project is licensed under the **MIT License**.

---

**Made for smart surveillance.**
