import cv2
import face_recognition
import numpy as np
from firebase_admin import db

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def open_video(callback):
    threshold = 0.6

    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Camera issue")
        return

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        encoded_face = face_recognition.face_encodings(faces)

        print(encoded_face)

        # Draw rectangles around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        callback(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


def getEncodedValues():
    persons_ref = db.reference('/persons')

    # Retrieve all data under '/persons'
    data = persons_ref.get()

    if data:
        # Iterate through the persons in the data
        for unique_id, person_data in data.items():
            if unique_id == '-O3kfugKdTDbj59ALNGc': #testing purpose
                try:
                    # Access the encodings list
                    encodings = person_data.get('encodings', [])
                    for encoding in encodings:
                        if isinstance(encoding, list):
                            # Process each encoding value (which is a list of floats)
                            print(f"Unique ID: {unique_id}, Encoding: {encoding}")
                            for value in encoding:
                                print(value)
                        elif encoding is None:
                            continue
                        else:
                            raise ValueError(f"Unexpected data type in encodings: {encoding}")
                    # Access the name
                    # name = person_data.get('name', '')
                    # if isinstance(name, str):
                    #     print(f"Unique ID: {unique_id}, Name: {name}")
                    # else:
                    #     raise ValueError(f"Unexpected data type for name: {name}")

                except ValueError as e:
                    print(f"Error processing data for {unique_id}: {e}")
    else:
        print("No data found.")