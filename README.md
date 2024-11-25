### Summary of the Code

This Python script implements a security system that uses face recognition to detect and identify people through a camera feed. Key features of the system include:

1. **Face Recognition**:
   - The script uses the `face_recognition` library to detect faces and compare them against a pre-existing list of known faces (stored in a pickle file).
   - If a known face is recognized, it displays the name and face distance (closeness) on the camera feed.
   - If an unknown face is detected, it triggers an alarm and sends an email notification.

2. **Alarm System**:
   - When an unknown face is detected, a sound alarm is played using Pygame (`alarm.wav`).
   - The alarm will continue until a known face is detected or the program is manually stopped.

3. **Email Notification**:
   - Upon detecting an unknown face, an email is sent to a predefined receiver with an attachment of the captured image of the unknown face.
   - Email is sent using Gmail's SMTP server with proper SSL encryption and authentication.

4. **Video Feed**:
   - The camera feed is processed in real-time, with faces detected and labeled either as "Known" or "Unknown".
   - A bounding box is drawn around the detected faces.

5. **Graceful Exit**:
   - The loop continues until the user presses the `q` key.
   - If the program is manually interrupted, resources are properly released using `finally`, ensuring the alarm stops, and the camera is released.

### Key Functions:
- **`find_closest_face`**: Compares the detected face against known faces and calculates the distance (similarity).
- **`play_alarm`** and **`stop_alarm`**: Control the playing and stopping of the alarm.
- **`send_email`**: Sends an email notification with an image attachment if an unknown face is detected.

### Error Handling:
- The code includes error handling for issues like missing model files, problems with face detection, and email sending errors.

### Flow:
1. The program captures the video feed and detects faces.
2. If a face is recognized, it shows the name and stops the alarm.
3. If the face is unknown, it triggers an alarm and sends an email with the image of the unknown face.
4. The program stops when the user presses `q` or the program is interrupted.

This solution provides a simple security monitoring system with real-time facial recognition and email notifications for unknown intruders.
