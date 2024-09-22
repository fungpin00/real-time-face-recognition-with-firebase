# Face Recognition Login System with Firebase

This project implements a face recognition-based login system using the Labeled Faces in the Wild \(LFW\) dataset. The system allows users to log in via traditional credentials \(username/password\) or by recognising their face in real-time using their webcam. The project integrates with Firebase for data storage and PyQt5 for the graphical user interface \(GUI\).

## Prerequisites
- **Python 3.x**: Ensure Python 3.6 or higher is installed, preferably not version after 3.10.15.
- **Firebase Project**: Set up a Firebase project and add Firebase Realtime Database.
- **Webcam**: A webcam is required for face recognition login.
## Installation

Follow these steps to set up the project on your machine:

### 1. Install Visual Studio with C++ Build Tools
`dlib` requires a C++ compiler. To install the necessary build tools:
- Download and install Visual Studio.
- During installation, select the "Desktop development with C++" workload.
- Ensure that you check the following options during installation:
  - C++ CMake tools for Windows
  - Windows SDK \(latest version compatible with your OS\)

### 2. Install Required Python Libraries
Ensure that you have `pip` installed on your system, then run the following commands to install the required libraries:

```bash
pip install opencv-python
pip install numpy
pip install firebase-admin
pip install cmake
pip install dlib
pip install face_recognition
pip install PyQt5
```

### 3. Firebase Configuration
- Set up a Firebase project.
- Create a Realtime Database and store user data \(including face encodings\) under a `/persons` reference.
- Download the Firebase Admin SDK JSON file for authentication.
- Place this JSON file in the project directory and update the path in the code:
  
```python
cred_obj = firebase_admin.credentials.Certificate("path/to/your-firebase-adminsdk.json")
```

## Features
- **Login via Credentials**: Users can log in using their username and password, securely stored in the Firebase Realtime Database.
- **Login via Face Recognition**: Users can log in by scanning their face using a webcam. The face recognition model compares the live feed with pre-stored encodings.
- **PyQt5 User Interface**: The system provides a custom login window designed with PyQt5, supporting both credential and face recognition login.
- **Password Hashing**: Passwords are stored securely in the database using SHA-256 hashing.
- **Firebase Integration**: User information, including username, hashed passwords, and face encodings, is stored in Firebase Realtime Database.

## Usage

### Running the Application
To start the application, run the following command:

```bash
python face_recognition_login.py
```

This will launch the login window, allowing users to choose between login methods.

- **Username/Password Login**: Enter your credentials and click "Login".
- **Face Recognition Login**: Click "Login with Face Recognition" to use the webcam for face-based authentication.

### Adding New Users
- Face encodings and user information must be pre-stored in Firebase. You can extend the system to add new users by adding face data using the `face_recognition` library and storing it in the Firebase database.

## Project Structure

```plaintext
├── config/
│   └── face-recognition-firebase-adminsdk.json  # Firebase credentials
├── images/
│   ├── login_background.jpg                    # Background for login UI
│   └── img.png                                 # Placeholder user icon
├── face_recog.py                               # Face recognition functions
├── login_ui.py                   # Main file to run the login system
└── README.md                                   # Project documentation
```

### Key Files
- **face_recog.py**: Contains the logic for performing face recognition.
- **face_recognition_login.py**: The main script to run the login system with PyQt5 GUI.
- **config/face-recognition-firebase-adminsdk.json**: Firebase configuration file.

## Face Recognition Flow

1. **Data Retrieval**: The face encodings for each user are retrieved from Firebase.
2. **Video Capture**: The system accesses the user's webcam and captures real-time video.
3. **Face Detection**: Using the `face_recognition` library, the system identifies faces in the video feed.
4. **Face Encoding Comparison**: The captured face is encoded and compared against the stored encodings using Euclidean distance.
5. **Login Decision**: If a face match is found, the user is logged in; otherwise, the system continues scanning.

## Library used

- **dlib**: For face detection and encoding.
- **Firebase**: For user authentication and data storage.
- **OpenCV**: For webcam interaction.
- **PyQt5**: For creating the GUI.
- **face_recognition**: For face detection and recognition functionality.

---

Feel free to customize and extend this project to meet specific needs, such as integrating new authentication methods or enhancing the GUI.
