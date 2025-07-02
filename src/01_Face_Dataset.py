# Topic: Face Recognition System - Part 1: Dataset Collection

'''
Part 1 of 3: Face Dataset Collection
Purpose: Create a dataset of face images for training the face recognition system
Process Flow:
    1. Capture multiple faces from different users
    2. Store images in Face_Dataset directory
    3. Each person gets a unique numeric ID
    4. Captures 30 different angles/expressions per person
File Naming: user.[ID].[IMAGE_NUMBER].jpg

Related Files:
- 02_Face_Training.py: Trains the model using these images
- 03_Face_Recognition.py: Uses the trained model for recognition
'''

import cv2
import os
import time

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
PATH_TO_DATASETS = os.path.join(PROJECT_ROOT, 'data', 'Face_Dataset')
HAARCASCADE_PATH = os.path.join(PROJECT_ROOT, 'static', 'haarcascade_frontalface_default.xml')
# Create dataset directory if it doesn't exist
if not os.path.exists(PATH_TO_DATASETS):
    os.makedirs(PATH_TO_DATASETS)
    print("[INFO] Face_Dataset directory created")

# Initialize video capture
cam = cv2.VideoCapture(0)  # Use external camera (0 for built-in webcam)
cam.set(3, 640)  # Set video width (property index 3)
cam.set(4, 480)  # Set video height (property index 4)

# Initialize face detector
face_detector = cv2.CascadeClassifier(HAARCASCADE_PATH)
if face_detector.empty():
    print(f"[ERROR] Failed to load Haar Cascade from {HAARCASCADE_PATH}")
    exit()
# Get user ID for dataset labeling
face_id = input('\nEnter user ID and press <return> ==>  ')

print("\n[INFO] Initializing face capture. Look at the camera and wait...")
count = 0  # Counter for number of face images

while(True):
    # Capture frame-by-frame
    ret, img = cam.read()
    img = cv2.flip(img, 1)  # Flip image horizontally for mirror effect
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the frame
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        # Draw rectangle around detected face
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
        count += 1

        # Save the captured face image
        cv2.imwrite(os.path.join(PATH_TO_DATASETS, f"user.{str(face_id)}.{str(count)}.jpg"), gray[y:y+h,x:x+w])

        # Display progress
        cv2.imshow('Face Collection - Progress: ' + str(count) + '/30', img)
    
    # Check for exit conditions
    k = cv2.waitKey(1) & 0xff
    if k == 27:  # ESC key to exit
        break
    elif count >= 30:  # Stop after collecting 30 images
        break

# Cleanup
cam.release()
cv2.destroyAllWindows()
print("\n[INFO] Dataset collection completed. 30 face images captured.")
