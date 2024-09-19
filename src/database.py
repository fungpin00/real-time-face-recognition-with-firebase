import firebase_admin
from firebase_admin import db

cred_obj = firebase_admin.credentials.Certificate(
    "../config/face-recognition-715e7-firebase-adminsdk-v67cv-446469e086.json")
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': 'https://face-recognition-715e7-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

persons_ref = db.reference('/persons')

# Retrieve all data under '/persons'
data = persons_ref.get()

global face_encodings
global face_names

if data:
    for unique_id, person_data in data.items():
        encodings = person_data.get('encodings', [])
        name = person_data.get('name', None)

        # Check if None is present in the encodings list
        if None in encodings:
            print(f"Cleaning up None encodings for {unique_id}")

            # Filter out None values
            valid_encodings = [encoding for encoding in encodings if encoding is not None]

            # Update the database with the cleaned encodings
            persons_ref.child(unique_id).update({'encodings': valid_encodings})

            print(f"Updated encodings for {unique_id}: {valid_encodings}")


def get_database_connection():
    return persons_ref



