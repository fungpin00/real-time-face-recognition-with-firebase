import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred_obj = firebase_admin.credentials.Certificate("face-recognition-715e7-firebase-adminsdk-v67cv-446469e086.json")
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': 'https://face-recognition-715e7-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

ref = db.reference('/')
users_ref = ref.child('users')
users_ref.set({
    'fungpin00': {
        'date_of_birth': 'June 23, 1912',
        'password': 'abc123'
    }
})


handle = db.reference('/users/fungpin00')

print(handle)



