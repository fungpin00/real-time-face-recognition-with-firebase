import time

import cv2
import face_recognition
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

        # Draw rectangles around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        callback(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


def get_known_encoded_values():
    known_encoded_values = {}
    persons_ref = db.reference('/persons')

    # Retrieve all data under '/persons'
    data = persons_ref.get()

    start_time = time.time()
    if data:
        # Iterate through the persons in the data
        for unique_id, person_data in data.items():
            try:
                # Access the encodings list
                encodings = person_data.get('encodings', [])
                if isinstance(encodings, list):
                    # Store the encodings list for each unique_id
                    known_encoded_values[unique_id] = [encoding for encoding in encodings if isinstance(encoding, list)]
                else:
                    raise ValueError(f"Unexpected data structure for encodings under {unique_id}: {encodings}")

            except ValueError as e:
                print(f"Error processing data for {unique_id}: {e}")
    else:
        print("No data found.")

    print(f"elapsed time : {time.time() - start_time}")
    return known_encoded_values


def get_known_names():
    persons_ref = db.reference('/persons')

    known_names = {}

    # Retrieve all data under '/persons'
    data = persons_ref.get()

    if data:
        # Iterate through the persons in the data
        for unique_id, person_data in data.items():
            try:
                # Access the name
                name = person_data.get('name', '')
                if isinstance(name, str):
                    known_names[unique_id] = name
                else:
                    raise ValueError(f"Unexpected data type for name under {unique_id}: {name}")
            except ValueError as e:
                print(f"Error processing data for {unique_id}: {e}")
    else:
        print("No data found.")

    return known_names
