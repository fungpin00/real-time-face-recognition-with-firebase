import hashlib
import sys

import firebase_admin.credentials
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QLabel, QCheckBox, QMessageBox
)
from firebase_admin import db

from face_recog import start_face_recognition

cred_obj = firebase_admin.credentials.Certificate(
    "../config/face-recognition-715e7-firebase-adminsdk-v67cv-446469e086.json")
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': 'https://face-recognition-715e7-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

person_ref = db.reference('/persons')


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Login')
        self.setFixedSize(400, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                font-family: 'Roboto', sans-serif;
                font-size: 14px;
                color: #333333;
            }
            QLineEdit {
                padding: 12px;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                margin-bottom: 20px;
            }
            QLineEdit:focus {
                border-color: #66AFE9;
                outline: none;
            }
            QPushButton {
                padding: 12px;
                background-color: #007BFF;
                color: #FFFFFF;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLabel#titleLabel {
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 40px;
            }
            QLabel#forgotPassword {
                color: #007BFF;
            }
            QLabel#forgotPassword:hover {
                color: #0056b3;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)

        # Title Label
        title = QLabel('Welcome Back!')
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName('titleLabel')
        main_layout.addWidget(title)

        # Username Field
        username_layout = QHBoxLayout()
        username_icon = QLabel()
        username_pixmap = QPixmap('user_icon.png').scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        username_icon.setPixmap(username_pixmap)
        username_field = QLineEdit()
        username_field.setPlaceholderText('Username')
        username_layout.addWidget(username_icon)
        username_layout.addWidget(username_field)
        main_layout.addLayout(username_layout)

        # Password Field
        password_layout = QHBoxLayout()
        password_icon = QLabel()
        password_pixmap = QPixmap('lock_icon.png').scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        password_icon.setPixmap(password_pixmap)
        password_field = QLineEdit()
        password_field.setPlaceholderText('Password')
        password_field.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(password_icon)
        password_layout.addWidget(password_field)
        main_layout.addLayout(password_layout)

        # Remember Me Checkbox and Forgot Password
        options_layout = QHBoxLayout()
        remember_me_checkbox = QCheckBox('Remember Me')
        options_layout.addWidget(remember_me_checkbox)
        options_layout.addStretch()
        forgot_password_label = QLabel('Forgot Password?')
        forgot_password_label.setObjectName('forgotPassword')
        options_layout.addWidget(forgot_password_label)
        main_layout.addLayout(options_layout)

        # Login Button
        login_button = QPushButton('Login')
        login_button.clicked.connect(lambda: self.login(username_field, password_field))
        main_layout.addWidget(login_button)

        # Or Separator
        or_layout = QHBoxLayout()
        or_layout.addWidget(self.create_line())
        or_label = QLabel('OR')
        or_label.setAlignment(Qt.AlignCenter)
        or_layout.addWidget(or_label)
        or_layout.addWidget(self.create_line())
        main_layout.addLayout(or_layout)

        # Face Recognition Login Button
        face_login_button = QPushButton('Login with Face Recognition')
        face_login_button.clicked.connect(self.face_login)
        face_login_button.setStyleSheet("""
            QPushButton {
                background-color: #28A745;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        main_layout.addWidget(face_login_button)

        # Spacer
        main_layout.addStretch()

        # Create Account Link
        signup_layout = QHBoxLayout()
        signup_label = QLabel("Don't have an account?")
        signup_link = QLabel('Sign Up')
        signup_link.setObjectName('forgotPassword')
        signup_layout.addStretch()
        signup_layout.addWidget(signup_label)
        signup_layout.addWidget(signup_link)
        signup_layout.addStretch()
        main_layout.addLayout(signup_layout)

        self.status = QLabel('')
        self.status.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status)

        self.setLayout(main_layout)

    def create_line(self):
        line = QLabel()
        line.setFrameShape(QLabel.HLine)
        line.setFrameShadow(QLabel.Sunken)
        line.setStyleSheet("color: #CCCCCC;")
        return line

    def login(self, username_field, password_field):
        # Implement your login logic here
        username = username_field.text()
        password = password_field.text()
        print(f"Login attempt - Username: {username}, Password: {password}")

        data = person_ref.get()
        login_flag = False
        for unique_id, person_data in data.items():
            current_username = person_data.get('username')
            if username.upper() == current_username.upper():
                current_password = person_data.get('password')
                if hashlib.sha256(password.encode()).hexdigest() == current_password:
                    login_flag = True
                    succesful_login_userID = unique_id
                    break

        if login_flag:
            print("Login success")
            self.open_main_menu(succesful_login_userID)
            self.hide()
        else:
            print("Login failed")

    def face_login(self):
        # This will trigger the face recognition process
        self.status.setText("Face recognition login initiated")
        successful_login_userID = start_face_recognition(person_ref)

        # if successful_login_userID:
        #     print("Face recognized. Proceeding to main menu.")
        #     self.open_main_menu(successful_login_userID)
        #     self.hide()  # Hide the login window after opening the main menu
        # else:
        #     print("Face recognition failed or no known face detected.")
        #     self.status.setText("Face recognition failed. Please try again.")

    def open_main_menu(self, user_id):
        print(f"Opening main menu for user_id: {user_id}")
        user_data = person_ref.child(user_id).get()
        if user_data:
            print("User data retrieved successfully.")
            self.main_menu_window = MainMenuWindow(user_data)
            self.main_menu_window.show()
        else:
            print("Failed to retrieve user data.")
            error_dialog = QMessageBox()
            error_dialog.setWindowTitle("Error")
            error_dialog.setText("Failed to open main menu. Please try again.")
            error_dialog.exec_()
            self.show()


class MainMenuWindow(QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.initUI()

    def initUI(self):
        try:
            print("Initializing MainMenuWindow UI.")
            self.setWindowTitle('Main Menu')
            self.setFixedSize(800, 600)
            self.setStyleSheet("""
                QWidget {
                    background-color: #f0f0f0;
                    font-family: 'Arial', sans-serif;
                    font-size: 14px;
                    color: #333333;
                }
                QLabel#titleLabel {
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 30px;
                }
                QPushButton {
                    padding: 12px 20px;
                    background-color: #007BFF;
                    color: #FFFFFF;
                    border: none;
                    border-radius: 5px;
                    font-size: 16px;
                    margin: 10px 0;
                }
                QPushButton:hover {
                    background-color: #0056b3;
                }
                QPushButton#logoutButton {
                    background-color: #DC3545;
                }
                QPushButton#logoutButton:hover {
                    background-color: #c82333;
                }
            """)

            main_layout = QVBoxLayout()
            main_layout.setContentsMargins(50, 50, 50, 50)
            main_layout.setSpacing(20)

            # Title Label
            welcome_label = QLabel(f"Welcome, {self.user_data.get('username', 'User')}!")
            welcome_label.setAlignment(Qt.AlignCenter)
            welcome_label.setObjectName('titleLabel')
            main_layout.addWidget(welcome_label)

            # Buttons Layout
            buttons_layout = QVBoxLayout()
            buttons_layout.setSpacing(15)

            # Logout Button
            logout_button = QPushButton('Logout')
            logout_button.setObjectName('logoutButton')
            logout_button.clicked.connect(self.logout)
            buttons_layout.addWidget(logout_button)

            # Add buttons layout to main layout
            main_layout.addLayout(buttons_layout)

            # Spacer
            main_layout.addStretch()

            self.setLayout(main_layout)
        except Exception as e:
            print(f"Exception in initUI: {e}")

    def logout(self):
        # Confirm logout action
        reply = QMessageBox.question(
            self, 'Logout', 'Are you sure you want to logout?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.close()
            if self.parent():
                self.parent().show()
            print("User logged out")
        else:
            print("Logout canceled")

    def closeEvent(self, event):
        # Handle window close event
        print("MainMenuWindow closed")
        super().closeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
