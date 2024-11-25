import numpy as np
import cv2
import pygame
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os
import pickle
import face_recognition

# Paths and Email configurations
email = "your_email@gmail.com"
password = "your_app_password"  # Use the app password created in Google Account
receiver_email = "receiver_email@gmail.com"
known_faces_model_path = "C:/Users/BALAJI/Downloads/Threat-Detection-System-main/models/home_owners.pkl"

# Load known faces model
try:
    with open(known_faces_model_path, 'rb') as f:
        known_faces = pickle.load(f)
except FileNotFoundError:
    print(f"Error: Known faces model not found at {known_faces_model_path}")
    exit(1)

# Initialize OpenCV DNN face detector and camera
protoPath = "C:/Users/BALAJI/Downloads/Threat-Detection-System-main/deploy.prototxt"
modelPath = "C:/Users/BALAJI/Downloads/Threat-Detection-System-main/res10_300x300_ssd_iter_140000_fp16.caffemodel"
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
camera = cv2.VideoCapture(0)

# Initialize Pygame for alarm
pygame.init()
alarm_sound = pygame.mixer.Sound('C:/Users/BALAJI/Downloads/Threat-Detection-System-main/alarm.wav')

def find_closest_face(vec, faces_list, threshold=0.5):
    min_distance = float("inf")
    closest_face = None
    for name, embeddings in faces_list.items():
        for embedding in embeddings:
            distance = np.linalg.norm(embedding - vec)
            if distance < min_distance:
                min_distance = distance
                closest_face = name
    return closest_face if min_distance < threshold else "Unknown", min_distance

def play_alarm():
    alarm_sound.play(-1)

def stop_alarm():
    alarm_sound.stop()

def send_email(subject, body, attachment=None, attachment_name=None):
    try:
        message = MIMEMultipart()
        message["From"] = email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))
        
        # Attach image if present
        if attachment is not None:
            with open(attachment, 'rb') as f:
                img_data = f.read()
            image = MIMEImage(img_data, name=attachment_name)
            message.attach(image)

        # Send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(email, password)
            server.sendmail(email, receiver_email, message.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print("Error sending email:", e)

# Main Loop
try:
    while True:
        ret, frame = camera.read()
        frame = cv2.resize(frame, (500, 500))
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect face locations
        face_locations = face_recognition.face_locations(rgb_frame, model="hog")
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            name, face_distance = find_closest_face(face_encoding, known_faces)

            if name != "Unknown":
                color = (0, 255, 0)  # Green for known faces
                cv2.putText(frame, f"{name} ({face_distance:.2f})", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                stop_alarm()
            else:
                color = (0, 0, 255)  # Red for unknown faces
                cv2.putText(frame, "Unknown", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                
                # Play alarm and send email once
                play_alarm()
                cv2.imwrite("unknown_face.png", frame)
                send_email("Unknown Face Detected", "An unknown face was detected on the security feed.", attachment="unknown_face.png", attachment_name="unknown_face.png")
                os.remove("unknown_face.png")

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

        # Display the frame with annotations
        cv2.imshow("Security Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Program interrupted manually.")
finally:
    # Cleanup
    stop_alarm()
    camera.release()
    cv2.destroyAllWindows()
    pygame.quit()
    print("Resources released and program terminated.")
