import firebase_admin
from firebase_admin import storage, db

cred_obj = firebase_admin.credentials.Certificate(
    "../config/face-recognition-715e7-firebase-adminsdk-v67cv-446469e086.json")
default_app = firebase_admin.initialize_app(cred_obj, {
    'storageBucket': 'face-recognition-715e7.appspot.com',
    'databaseURL': 'https://face-recognition-715e7-default-rtdb.asia-southeast1.firebasedatabase.app/'
})


import os

lfw_dir = 'C:/Users/fungp/Downloads/archive/lfw-deepfunneled/lfw-deepfunneled'

data = db.reference('/persons').get()


def upload_images_for_person(image_folder_path, name_to_id_map):
    """
    Uploads all images in a folder to Firebase Storage for a specific person using an efficient lookup map.

    :param image_folder_path: The folder containing the images for a specific person.
    :param name_to_id_map: A dictionary mapping person names (folder names) to unique Firebase IDs.
    """
    counter = 0

    # Iterate over the person directories in the provided image folder
    for person_name in os.listdir(image_folder_path):
        person_dir = os.path.join(image_folder_path, person_name)

        # Get the corresponding unique_id using the pre-built dictionary
        unique_id = name_to_id_map.get(person_name)

        # If no matching unique_id is found, skip this person
        if not unique_id:
            print(f"No unique_id found for person: {person_name}, skipping...")
            continue

        # Now process the images for the matched person
        for image_name in os.listdir(person_dir):
            if image_name.endswith(".jpg") or image_name.endswith(".png"):
                # Get the full path of the image file
                image_path = os.path.join(person_dir, image_name)

                # Use the filename (without the extension) as the image ID
                image_id = os.path.splitext(image_name)[
                    0]  # Example: if filename is '0001.jpg', image_id will be '0001'
                counter += 1

                # Debugging information
                print(f"Counter: {counter} Image ID: {image_id}")
                print(f"Counter: {counter} Image Path: {image_path}")
                print(f"Counter: {counter} Unique ID: {unique_id}")

                # Upload the image to Firebase Storage (uncomment when you're ready)
                upload_image_to_firebase(image_path, unique_id, image_id)


# Preprocess Firebase data to create a mapping of person_name -> unique_id
def create_name_to_id_map(data):
    name_to_id_map = {}
    for unique_id, person_data in data.items():
        person_name = person_data.get('name')
        if person_name:
            name_to_id_map[person_name] = unique_id
    return name_to_id_map

def upload_image_to_firebase(image_path, person_id, image_id):
    # Get the Firebase Storage bucket
    bucket = storage.bucket()

    # Create a blob (storage reference) with a path in the storage
    blob = bucket.blob(f"faces/{person_id}/{image_id}.jpg")

    # Upload the image file to Firebase Storage
    blob.upload_from_filename(image_path)

    # Get the image's download URL
    blob.make_public()
    download_url = blob.public_url

    # Update the Firebase Realtime Database with the image URL
    ref = db.reference(f'persons/{person_id}/images/{image_id}')
    ref.set({
        'url': download_url
    })

    print(f"Image {image_id} uploaded for {person_id}: {download_url}")
    return download_url


name_to_id_map = create_name_to_id_map(data)

upload_images_for_person(lfw_dir, name_to_id_map)