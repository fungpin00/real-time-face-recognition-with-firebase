import firebase_admin
from firebase_admin import db

cred_obj = firebase_admin.credentials.Certificate(
    "../config/face-recognition-715e7-firebase-adminsdk-v67cv-446469e086.json")
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': 'https://face-recognition-715e7-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

persons_ref = db.reference('/persons')

for unique_iid in str(persons_ref.get()):
    print(unique_iid)
