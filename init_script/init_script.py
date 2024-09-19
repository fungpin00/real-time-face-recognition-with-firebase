import datetime
import os

import face_recognition
import firebase_admin
from firebase_admin import db
from firebase_admin import storage
import hashlib
cred_obj = firebase_admin.credentials.Certificate(
    "../config/face-recognition-715e7-firebase-adminsdk-v67cv-446469e086.json")
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': 'https://face-recognition-715e7-default-rtdb.asia-southeast1.firebasedatabase.app/',
    'storageBucket': 'face-recognition-715e7.appspot.com'  # Your storage bucket
})

person_ref = db.reference('/persons')

def create_new_user_with_image(username, password, file_path):
    # Reference the Firebase storage bucket
    bucket = storage.bucket()

    # Create a blob (storage object) for the image
    image_blob = bucket.blob(f"images/{os.path.basename(file_path)}")

    # Upload the image to Firebase Storage
    image_blob.upload_from_filename(file_path)

    # Generate a signed URL for temporary access to the image (valid for 5 minutes)
    expiration_time = datetime.timedelta(minutes=5)
    image_url = image_blob.generate_signed_url(expiration=expiration_time)

    print(f"Image uploaded to Firebase Storage: {image_url}")

    # Creating a new user in the Realtime Database
    user_ref = person_ref.push()  # Generates a unique key for the new user

    # Hash the password before storing (for security purposes)
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # List to store the face encodings (since a user could have multiple images in the future)
    person_encodings = []

    # Load the image and extract the face encoding using face_recognition
    image = face_recognition.load_image_file(file_path)
    face_encodings = face_recognition.face_encodings(image)

    # Check if there are any face encodings detected in the image
    if face_encodings:
        # Convert the NumPy array to a list for JSON serialization
        for i, encoding in enumerate(face_encodings):
            person_encodings.append(encoding.tolist())  # Store each face encoding as a list

        # Print debugging information
        print(f"Username: {username}, Password: {password}, encodings: {person_encodings}")
    else:
        print("No face detected in the image.")
        person_encodings = None

    # Prepare the encodings data to be saved in the database
    encodings_data = {str(i): encoding for i, encoding in enumerate(person_encodings)} if person_encodings else {}

    # Set user information in the Realtime Database
    user_ref.set({
        'username': username,
        'password': hashed_password,  # Store the hashed password
        'images': image_url,  # Store signed URL (valid for 5 minutes)
        'encodings': encodings_data,  # Face encoding data (starting at index 0)
        'name': username
    })

    print(f"New user {username} created successfully with user_id: {user_ref.key}")

# def delete_all_records():
#     person_ref.delete()
#     print("All records are deleted")
#
#
# # clear data first
# delete_all_records()

# lfw_dir = '../data'
# known_face_data = {}  # Dictionary to store names and their encodings
# count = 0
#
#
# for person_name in os.listdir(lfw_dir):
#     person_dir = os.path.join(lfw_dir, person_name)
#
#     person_encodings = []
#     for image_name in os.listdir(person_dir):
#         image_path = os.path.join(person_dir, image_name)
#
#         image = face_recognition.load_image_file(image_path)
#         face_encodings = face_recognition.face_encodings(image)
#
#         if face_encodings:
#             person_encodings.append(face_encodings[0].tolist())
#
#     if person_encodings:
#         known_face_data[person_name] = person_encodings
#         count += 1
#         print(count)
#
# # Create a reference to the 'persons' node in the database
# persons_ref = person_ref.child('persons')
#
# # Add each person with their encodings to the database
# for name, encodings in known_face_data.items():
#     # Create a new child node with a unique key
#     new_person_ref = persons_ref.push()
#
#     # Prepare the encodings data
#     encodings_data = {str(i + 1): encoding for i, encoding in enumerate(encodings)}
#
#     # Set the data for this person
#     new_person_ref.set({
#         'name': name,
#         'encodings': encodings_data
#     })
#
#     print(f"Added {name} to the database with {len(encodings)} encodings")
#
# print("All persons have been added to the database with their encodings")


if __name__ == '__main__':
    # Example usage
    # Path to the image file to upload
    image_path = 'C:/Users/fungp/PycharmProjects/face-recognition-with-lfw-dataset/images/fungpin.jpg'

    # New user information
    new_username = 'fungpin'
    new_password = 'fungpin123'

    # Call the function to create the new user with image
    create_new_user_with_image(new_username, new_password, image_path)