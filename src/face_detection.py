import face_recognition
import cv2
import os


lfw_dir = 'C:/Users/fungp/OneDrive/Desktop/ai/lfw_funneled'

known_face_encodings = []
known_face_names = []
count = 0
limit = 2

for person_name in os.listdir(lfw_dir):

    person_dir = os.path.join(lfw_dir, person_name)

# Iterate through each image of the person
    for image_name in os.listdir(person_dir):
        if count >= limit:
            break
        image_path = os.path.join(person_dir, image_name)

    # Load the image
        image = face_recognition.load_image_file(image_path)
        showimage = cv2.imread(image_path)
    # Encode the face
        face_encodings = face_recognition.face_encodings(image)

        if face_encodings:  # If at least one face was found
            known_face_encodings.append(face_encodings[0])
            known_face_names.append(person_name)
            count += 1
            cv2.putText(showimage,person_name,(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),1)
            cv2.imshow('Image', showimage)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


print(f"Loaded {len(known_face_encodings)} face encodings.")


