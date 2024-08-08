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

if data:
    # Iterate through the persons in the data
    for unique_id, person_data in data.items():
        if unique_id == '-O3kfugKdTDbj59ALNGc':
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
                name = person_data.get('name', '')
                if isinstance(name, str):
                    print(f"Unique ID: {unique_id}, Name: {name}")
                else:
                    raise ValueError(f"Unexpected data type for name: {name}")

            except ValueError as e:
                print(f"Error processing data for {unique_id}: {e}")
else:
    print("No data found.")

