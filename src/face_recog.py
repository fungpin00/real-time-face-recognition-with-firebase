import cv2
import face_recognition
import numpy as np

FACE_DISTANCE_THRESHOLD = 0.4
model_list = ["cnn","hog"]
MODEL = "cnn"
MIN_FACE_SIZE = 20


def start_face_recognition(db_reference):
    data = db_reference.get()
    if data:
        existing_face_encodings = {}
        existing_face_name = {}
        # todo (change count if want to include everyone's encoding)
        count = 0
        limit = 99999
        for unique_id, person_data in data.items():
            if count >= limit:
                break
            encodings = person_data.get('encodings', [])
            name = person_data.get('name', None)

            valid_encodings = [encoding for encoding in encodings if encoding is not None]

            existing_face_encodings[unique_id] = valid_encodings
            existing_face_name[unique_id] = name
            count += 1
    # limit data for performance
    count = 0
    limit = 99999
    all_encodings = []
    all_names = []
    all_unique_ids = []

    for unique_id, encodings_list in existing_face_encodings.items():
        if count >= limit:
            break
        name = existing_face_name[unique_id]
        for encoding in encodings_list:
            all_encodings.append(encoding)
            all_names.append(name)
            all_unique_ids.append(unique_id)
            count += 1

    video_capture = cv2.VideoCapture(0)

    face_locations = []
    face_names = []
    process_this_frame = True
    consecutive_matches = 0
    required_matches = 5
    for unique_id, encodings_list in existing_face_encodings.items():
        valid_encodings = [np.array(encoding) for encoding in encodings_list]
        existing_face_encodings[unique_id] = valid_encodings

    while True:
        name = "Unknown"
        ret, frame = video_capture.read()

        if process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_small_frame, model=model_list[0])
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
                    consecutive_matches += 1
                    if consecutive_matches >= required_matches:
                        video_capture.release()
                        cv2.destroyAllWindows()
                        return known_user_id
                else:
                    name = "Unknown"
                    consecutive_matches = 0
                face_names.append(name)

        process_this_frame = not process_this_frame

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            if (bottom - top) < MIN_FACE_SIZE or (right - left) < MIN_FACE_SIZE:
                continue
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            if name != "Unknown":
                color = (0, 255, 0)
            else:
                color = (0, 0, 255)

            cv2.rectangle(frame, (left, top), (right, bottom), color,2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Face recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if name != "Unknown":
            video_capture.release()
            cv2.destroyAllWindows()
            return known_user_id
