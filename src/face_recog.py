import cv2
import face_recognition
import numpy as np

FACE_DISTANCE_THRESHOLD = 0.45
model_list = ["cnn","hog"]

def start_face_recognition(db_reference):
    data = db_reference.get()
    if data:
        existing_face_encodings = {}
        existing_face_name = {}
        count = 0
        limit = 20
        for unique_id, person_data in data.items():
            if count >= limit:
                break
            # Retrieve the encodings and name
            encodings = person_data.get('encodings', [])
            name = person_data.get('name', None)

            # Filter out any None values
            valid_encodings = [encoding for encoding in encodings if encoding is not None]

            # Store the valid encodings and name
            existing_face_encodings[unique_id] = valid_encodings
            existing_face_name[unique_id] = name
            count += 1
    # limit data for performance
    count = 0
    limit = 20
    all_encodings = []
    all_names = []
    all_unique_ids = []

    for unique_id, encodings_list in existing_face_encodings.items():
        if count >= limit:
            break
        name = existing_face_name[unique_id]  # Get the corresponding name
        for encoding in encodings_list:
            all_encodings.append(encoding)  # Add each encoding to the flat list
            all_names.append(name)  # Add the corresponding name for each encoding
            all_unique_ids.append(unique_id)  # Add the unique_id
            count += 1

    video_capture = cv2.VideoCapture(0)

    # Load a sample picture and learn how to recognize it.

    # Create arrays of known face encodings and their names
    # Initialize some variables
    face_locations = []
    face_names = []
    process_this_frame = True

    for unique_id, encodings_list in existing_face_encodings.items():
        valid_encodings = [np.array(encoding) for encoding in encodings_list]
        existing_face_encodings[unique_id] = valid_encodings

    while True:
        name = "Unknown"
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Only process every other frame of video to save time
        if process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_small_frame, model=model_list[1])
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # use the known face with the smallest distance to the new face euclidean distances
                # of face for two vector
                face_distances = face_recognition.face_distance(all_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                if face_distances[best_match_index] < FACE_DISTANCE_THRESHOLD:
                    name = all_names[best_match_index]
                    known_user_id = all_unique_ids[best_match_index]
                else:
                    name = "Unknown"
                face_names.append(name)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Change color based on recognition status
            if name != "Unknown":
                color = (0, 255, 0)  # Green for known faces
            else:
                color = (0, 0, 255)  # Red for unknown faces

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # if name != "Unknown":
        #     video_capture.release()
        #     cv2.destroyAllWindows()
        #     return known_user_id
