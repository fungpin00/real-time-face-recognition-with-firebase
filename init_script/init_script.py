#!/usr/bin/env python3
import os

import face_recognition
import firebase_admin
from firebase_admin import db

cred_obj = firebase_admin.credentials.Certificate(
    "../config/face-recognition-715e7-firebase-adminsdk-v67cv-446469e086.json")
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': 'https://face-recognition-715e7-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

person_ref = db.reference('/')


# def delete_all_records():
#     person_ref.delete()
#     print("All records are deleted")
#
#
# # clear data first
# delete_all_records()

lfw_dir = '../data'
known_face_data = {}  # Dictionary to store names and their encodings
count = 0


for person_name in os.listdir(lfw_dir):
    person_dir = os.path.join(lfw_dir, person_name)

    person_encodings = []
    for image_name in os.listdir(person_dir):
        image_path = os.path.join(person_dir, image_name)

        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)

        if face_encodings:
            person_encodings.append(face_encodings[0].tolist())

    if person_encodings:
        known_face_data[person_name] = person_encodings
        count += 1
        print(count)

# Create a reference to the 'persons' node in the database
persons_ref = person_ref.child('persons')

# Add each person with their encodings to the database
for name, encodings in known_face_data.items():
    # Create a new child node with a unique key
    new_person_ref = persons_ref.push()

    # Prepare the encodings data
    encodings_data = {str(i + 1): encoding for i, encoding in enumerate(encodings)}

    # Set the data for this person
    new_person_ref.set({
        'name': name,
        'encodings': encodings_data
    })

    print(f"Added {name} to the database with {len(encodings)} encodings")

print("All persons have been added to the database with their encodings")
