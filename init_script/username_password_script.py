import firebase_admin
from firebase_admin import credentials, db
import hashlib

cred_obj = firebase_admin.credentials.Certificate(
    "../config/face-recognition-715e7-firebase-adminsdk-v67cv-446469e086.json")
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': 'https://face-recognition-715e7-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def update_username_password():
    person_ref = db.reference('/persons')
    data = person_ref.get()

    if data:
        for unique_id,person_data in data.items():
            name = person_data.get('name',None)
            if name:
                username = name + '123'
                password = 'abc123'
                hashed_password = hash_password(password)

                person_ref.child(unique_id).update({
                    'username': username,
                    'password': hashed_password
                })

if __name__ == "__main__":
    update_username_password()