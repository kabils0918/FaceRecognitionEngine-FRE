# AI CCTV Security System with Face Recognition & Alerting

## Project Overview

This project implements a robust real-time face recognition security system designed for surveillance applications, particularly in identifying individuals categorized as "terrorists." The system captures video feed, detects faces, recognizes known individuals using a trained model, and triggers various alerts (visual, audio, email, and SMS) upon the detection of a high-priority individual. It also features a Flask-based web dashboard for live monitoring of detections, historical logs, and managing captured snapshots.

## Features

* **Real-time Face Detection:** Utilizes Haar Cascades to detect faces in live video streams.
* **Face Recognition:** Employs the Local Binary Patterns Histograms (LBPH) algorithm for robust face recognition.
* **Dataset Collection:** Dedicated script for easily collecting new face datasets for training.
* **Model Training:** A separate script to train the LBPH model from the collected datasets.
* **Alerting System:**
    * **Visual Alerts:** On-screen notifications during detection.
    * **Audio Alarm:** Plays an alarm sound (`alarm.wav`) upon detecting a "terrorist."
    * **Email Notifications:** Sends an email with detection details and a captured image of the detected "terrorist."
    * **SMS Alerts:** Sends an SMS notification via Twilio upon detecting a "terrorist."
* **Web Dashboard (Flask):**
    * Real-time display of the latest detection.
    * Table view of all detection logs.
    * Visual representation of detection trends over time.
    * Ability to download the full detection log as a CSV.
    * Options to clear the latest detection log/image or all logs/images.
* **Data Persistence:** Logs all detections to a CSV file (`detection_log.csv`) and saves captured images.

## Technologies Used

* **Python 3.x**
* **OpenCV:** For real-time video processing, face detection, and recognition.
* **Flask:** Web framework for the dashboard.
* **Pillow (PIL):** For image processing (used by OpenCV internally).
* **Numpy:** For numerical operations.
* **pygame:** For playing alarm sounds.
* **Twilio:** For sending SMS alerts.
* **smtplib:** For sending email alerts.
* **python-dotenv:** For managing environment variables securely.
* **Chart.js:** For interactive data visualization on the dashboard.

## Project Structure
.
├── .vscode/                     # VS Code configuration (optional, can be ignored by Git)
├── data/                        # Contains application data
│   ├── Face_datasets/           # Stores captured face images for training (e.g., user.1.1.jpg)
│   └── trainer/                 # Stores the trained face recognition model
│       └── trainer.yml          # The trained LBPH model file
│   └── detection_log.csv        # CSV log of all face detections
├── env_temp/                    # Python virtual environment (recommended to be ignored by Git)
│   ├── Include/
│   ├── Lib/
│   ├── Scripts/
│   │   └── activate             # Script to activate the virtual environment on Windows
│   └── pyvenv.cfg
├── src/                         # Source code for the core face recognition logic
│   ├── 01_Face_Dataset.py       # Script for collecting face datasets
│   ├── 02_Face_Training.py      # Script for training the face recognition model
│   └── 03_Face_Recognition.py   # Script for real-time face recognition and alerts
├── static/                      # Static files for the Flask web application
│   ├── alarm.wav                # Alarm sound file played on terrorist detection
│   ├── captured_faces/          # Parent directory for captured face images
│   │   └── Terrorist_Data/      # Stores images captured during "terrorist" detection
│   │       └── auto_capture_YYYYMMDD-HHMMSS.jpg # Example captured image
│   ├── haarcascade_frontalface_default.xml # Haar Cascade classifier XML for face detection
│   └── templates/               # HTML templates for the Flask app
│       └── dashboard.html       # HTML template for the web dashboard
├── venv/                        # Another Python virtual environment (can also be ignored by Git)
├── .env                         # Environment variables (e.g., API keys, email credentials)
├── .gitignore                   # Specifies files/folders to be ignored by Git
├── app.py                       # Main Flask application for the web dashboard
├── requirements.txt             # Python dependencies for the project
└── run_project.bat              # Batch script to set up and run the entire system on Windows

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

* **Python 3.x:** Download and install from [python.org](https://www.python.org/).
* **Git:** Download and install from [git-scm.com](https://git-scm.com/).
* **Webcam:** A functional webcam is required for face detection.
* **Internet Connection:** Required for installing dependencies and sending alerts (email/SMS).

### 1. Clone the Repository

```bash
git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
cd your-repository-name
(Replace https://github.com/your-username/your-repository-name.git with your actual repository URL).

2. Set Up Virtual Environment
It's highly recommended to use a virtual environment to manage project dependencies.
This project uses env_temp.

python -m venv env_temp

Activate the virtual environment:
On Windows (Command Prompt/PowerShell):
.\env_temp\Scripts\activate

On macOS/Linux (Bash/Zsh):
source env_temp/bin/activate

3. Install Dependencies
With your virtual environment activated, install all required Python packages:
pip install -r requirements.txt
4. Configure Environment Variables (.env)
Create a file named .env in the root directory of your project. This file will store sensitive credentials for email and Twilio.

Example .env content:
EMAIL_PASSWORD="your_gmail_app_password"
TWILIO_SID="ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
TWILIO_AUTH_TOKEN="your_twilio_auth_token"
TWILIO_PHONE_NUMBER="+1234567890" # Your Twilio phone number (e.g., +15017122661)

EMAIL_PASSWORD: For sending emails via Gmail, you need an App Password, not your regular Gmail password. Generate one from your Google Account security settings.
TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER: Obtain these from your Twilio account dashboard.

5. Ensure Static Assets are Present
static/haarcascade_frontalface_default.xml: This file should already be in your repository. It's essential for face detection.

static/alarm.wav: Ensure this alarm sound file is present in the static/ directory.

Usage
1. Collect Face Dataset
You need to collect images of individuals you want the system to recognize.
Run 01_Face_Dataset.py from the src directory.

# Ensure your virtual environment is active
python src/01_Face_Dataset.py

The script will prompt you to enter a User ID. Enter a unique integer ID for each person.

Look at the camera, and it will capture 30 images of your face, saving them in data/Face_datasets/.

2. Train the Face Recognition Model
After collecting datasets for all individuals, train the model.
Run 02_Face_Training.py from the src directory.

# Ensure your virtual environment is active
python src/02_Face_Training.py

This script will read the images from data/Face_datasets/, train the LBPH model, and save the trainer.yml file in data/trainer/.

3. Run the Entire System
The run_project.bat script is provided for convenience to start both the face recognition logic and the Flask dashboard simultaneously.
# On Windows, from the project root:
run_project.bat

This will open two command prompt windows:
1. One running 03_Face_Recognition.py, which will start your webcam feed.
2. One running app.py, which will start the Flask web server.

Alternatively, you can run them manually:

Open a new command prompt/terminal (with virtual env activated):
python src/03_Face_Recognition.py
Open another new command prompt/terminal (with virtual env activated):
python app.py

4. Access the Dashboard
Once app.py is running, open your web browser and go to:
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

Dashboard Features
The dashboard provides a user-friendly interface to monitor the system:
Latest Detection: Displays details and an image of the most recently detected person.
Detection Table: Shows a chronological log of all detections, including timestamp, name/ID, category, and a link to the captured image.
Search Functionality: Filter detection logs by ID or category.
Detection Trend Graph: A line graph showing the number of detections per day.
Download Log: Option to download detection_log.csv.

Clear Data:
Clear Latest Snapshot: Removes the last entry from detection_log.csv and deletes its corresponding image from static/captured_faces/Terrorist_Data/.
Clear All Snapshots: Clears all entries from detection_log.csv and deletes all captured images from static/captured_faces/Terrorist_Data/.

Alerting System Details
Terrorist Detection: If a person categorized as "terrorist" is detected by 03_Face_Recognition.py:
An audible alarm.wav sound will play.
An email will be sent to the configured receiver with incident details and a captured image.
An SMS will be sent via Twilio with a brief alert message.

https://github.com/user-attachments/assets/e923df64-3ffc-4e2d-b7a9-f887caa0a7a0


The event will be logged in detection_log.csv and the image saved in static/captured_faces/Terrorist_Data/.

Contributing
Feel free to fork the repository, open issues, or submit pull requests.

License
This project is open-source and available under the MIT License.
