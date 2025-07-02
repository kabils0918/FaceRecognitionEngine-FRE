# Topic: Face Recognition System - Part 2: Model Training

'''
Part 2 of 3: Face Recognition Training
Purpose: Train the LBPH Face Recognizer using collected face dataset
Process Flow:
    1. Load face images from Face_Dataset directory
    2. Convert images to grayscale and detect faces
    3. Train LBPH (Local Binary Pattern Histogram) recognizer
    4. Save trained model as trainer.yml

Dependencies:
    - Face_Dataset directory with images from 01_Face_Dataset.py
    - Haar Cascade classifier for face detection
    - OpenCV's LBPH Face Recognizer

Output:
    - trainer.yml: Trained model file used by 03_Face_Recognition.py
'''

import cv2
import numpy as np
from PIL import Image
import os

# Define paths relative to the script's location (inside src/)
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
# CHANGED: 'Face_Dataset' to 'Face_datasets'
PATH_TO_TRAINER = os.path.join(PROJECT_ROOT, 'data','trainer.yml')
HAARCASCADE_PATH = os.path.join(PROJECT_ROOT, 'static', 'haarcascade_frontalface_default.xml')
DATASET_PATH = os.path.join(PROJECT_ROOT, 'data', 'Face_dataset')

# Create trainer directory if it doesn't exist
if not os.path.exists(PATH_TO_TRAINER):
    os.makedirs(PATH_TO_TRAINER)
    print("[INFO] trainer directory created")

# Path for face image database
path = DATASET_PATH

# Initialize LBPH Face Recognizer and Cascade Classifier
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(HAARCASCADE_PATH)

def getImagesAndLabels(pathh):
    """
    Load and prepare face images for training
    Args:
        path: Directory containing face images
    Returns:
        faceSamples: List of face images
        ids: List of corresponding user IDs
    """
    # Get all image paths
    imagePaths = [os.path.join(pathh,f) for f in os.listdir(pathh)]     
    faceSamples = []
    ids = []

    for imagePath in imagePaths:
        # Load image and convert to grayscale
        PIL_img = Image.open(imagePath).convert('L')
        img_numpy = np.array(PIL_img, 'uint8')

        # Extract user ID from filename
        #id = int(os.path.split(imagePath)[-1].split(".")[1])
        xy = os.path.split(imagePath)[-1]
        #print(xy)
        xyz = xy.split(".")
        #print(xyz)
        #print(xyz[1])
        id = int(xyz[1])
        # Detect faces in the image
        faces = detector.detectMultiScale(img_numpy)

        # Add each face and ID to training set
        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)
            #print(ids)
            #print(faceSamples)

    return faceSamples, ids

print("\n[INFO] Training faces. It will take a few seconds. Wait ...")
abc = getImagesAndLabels(path)
faces, ids = abc
recognizer.train(faces, np.array(ids))

# Save the model
model_path = PATH_TO_TRAINER
recognizer.write(model_path)

# Print training summary
print(f"\n[INFO] {len(np.unique(ids))} faces trained successfully!")
print(f"[INFO] Model saved as: {model_path}")
print("[INFO] Training completed. You can now use 03_Face_Recognition.py")

