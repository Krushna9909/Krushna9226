import face_recognition
import cv2
import os
import numpy as np
import pandas as pd
from datetime import datetime

# Create a directory to store known faces
if not os.path.exists("students"):
    os.makedirs("students")

# Function to capture a student's face and save the encoding
def capture_face(student_name):
    video_capture = cv2.VideoCapture(0)  # Use the first camera
    
    # Allow the camera to warm up
    print("Capturing image for", student_name)
    
    while True:
        ret, frame = video_capture.read()
        
        # Detect faces in the frame
        face_locations = face_recognition.face_locations(frame)
        
        # If faces are detected
        if len(face_locations) > 0:
            face_encoding = face_recognition.face_encodings(frame, face_locations)[0]
            np.save(f"students/{student_name}_encoding.npy", face_encoding)
            print(f"Face encoding for {student_name} saved.")
            break
        
        # Display the captured frame
        cv2.imshow("Capture Face", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
            break
    
    video_capture.release()
    cv2.destroyAllWindows()

# Function to mark attendance
def mark_attendance(student_name):
    with open('attendance.csv', 'a') as f:
        f.write(f"{student_name},{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Load known face encodings
known_face_encodings = []
known_face_names = []

# Load stored face encodings from the students directory
for file in os.listdir("students"):
    if file.endswith("_encoding.npy"):
        name = file.split("_")[0]
        encoding = np.load(f"students/{file}")
        known_face_encodings.append(encoding)
        known_face_names.append(name)

# Start video capture
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    
    # Find all face locations and encodings in the frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Compare the detected face with known faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        
        # If a match is found, get the name
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
        
        # Mark attendance if the student is recognized
        mark_attendance(name)
        
        # Draw a rectangle around the face and label it
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
    
    # Display the video feed
    cv2.imshow('Video', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break

video_capture.release()
cv2.destroyAllWindows()
