import hashlib
import sys

import firebase_admin.credentials
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtWidgets import (
    QApplication, QMessageBox
)
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QCheckBox, QGraphicsDropShadowEffect, QGraphicsOpacityEffect, QFrame)
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
        self.setFixedSize(800, 600)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Create main widget and apply shadow
        main_widget = QWidget(self)
        main_widget.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                border-radius: 10px;
                font: 14px bold 'Segoe UI';
            }
        """)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 0)
        main_widget.setGraphicsEffect(shadow)

        # Main layout
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Ensure no margins
        main_layout.setSpacing(0)  # Remove any spacing between widgets

        # Left side (illustration)
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)  # Remove all margins
        left_layout.setSpacing(0)  # Remove any internal spacing

        illustration = QLabel()
        pixmap = QPixmap("../images/login_background.jpg")  # Your uploaded image
        illustration.setPixmap(
            pixmap.scaled(500, 700, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        left_layout.addWidget(illustration, alignment=Qt.AlignLeft | Qt.AlignTop)

        # Apply 50% opacity
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.95)  # 50% transparency
        illustration.setGraphicsEffect(opacity_effect)

        # Make sure the left widget background is transparent
        left_widget.setStyleSheet("background-color: transparent;")

        main_layout.addWidget(left_widget)

        # Right side (login form)
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(20, 20, 20, 20)

        # Close button
        close_button = QPushButton("×")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #000000;
                font-size: 20px;
                border: none;
            }
            QPushButton:hover {
                color: #FF0000;
            }
        """)
        close_button.clicked.connect(self.close)
        right_layout.addWidget(close_button, alignment=Qt.AlignRight)

        # Logo
        logo_label = QLabel("Login")
        logo_label.setAlignment(Qt.AlignLeft)
        logo_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        right_layout.addWidget(logo_label)
        logo_label.setStyleSheet("""
            QLabel{
                font: 18px bold 'Segoe UI';
            }
        """)
        logo_label.setAlignment(Qt.AlignCenter)

        # User icon
        user_icon = QLabel()
        user_pixmap = QPixmap("../images/img.png")  # Replace with your user icon
        user_icon.setPixmap(user_pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        right_layout.addWidget(user_icon, alignment=Qt.AlignCenter)

        # Username field
        self.username_field = QLineEdit()
        self.username_field.setPlaceholderText("Username")
        right_layout.addWidget(self.username_field)
        right_layout.addWidget(self.username_field, alignment=Qt.AlignRight)
        self.username_field.setStyleSheet("""
             QLineEdit{
                width:400px;
                font: 14px 'Segoe UI';
             }
        """)

        def on_username_focus_in(event):
            if self.username_field.placeholderText() == "Username":
                self.username_field.setPlaceholderText("")
            QLineEdit.focusInEvent(self.username_field, event)

        # Override the focusOutEvent to restore the placeholder text if empty
        def on_username_focus_out(event):
            if not self.username_field.text():
                self.username_field.setPlaceholderText("Username")
            QLineEdit.focusOutEvent(self.username_field, event)

        # Connect the events for username field
        self.username_field.focusInEvent = on_username_focus_in
        self.username_field.focusOutEvent = on_username_focus_out

        # Password field
        self.password_field = QLineEdit()
        self.password_field.setPlaceholderText("Password")
        self.password_field.setEchoMode(QLineEdit.Password)
        right_layout.addWidget(self.password_field, alignment=Qt.AlignRight)
        self.password_field.setStyleSheet("""
            QLineEdit{
                width:400px;
                font: 14px 'Segoe UI';
             }
        """)

        def on_focus_in(event):
            if self.password_field.placeholderText() == "Password":
                self.password_field.setPlaceholderText("")
            QLineEdit.focusInEvent(self.password_field, event)

        # Override the focusOutEvent to restore the placeholder text if empty
        def on_focus_out(event):
            if not self.password_field.text():
                self.password_field.setPlaceholderText("Password")
            QLineEdit.focusOutEvent(self.password_field, event)

        # Connect the events
        self.password_field.focusInEvent = on_focus_in
        self.password_field.focusOutEvent = on_focus_out

        # Login button
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)
        right_layout.addWidget(login_button, alignment=Qt.AlignCenter)
        login_button.setStyleSheet("""
        QPushButton {
            color: #000000;
            background-color: #85def1;
            width: 200px;
            border: 1.5px solid black;
        }
        QPushButton:hover {
            background-color: #9de5f4;
        }""")

        # Error message label (initially hidden)
        self.error_message = QLabel("")
        self.error_message.setAlignment(Qt.AlignCenter)
        self.error_message.setStyleSheet("color: red; font-size: 14px;")
        right_layout.addWidget(self.error_message)

        or_layout = QHBoxLayout()
        or_layout.addWidget(self.create_line())
        or_label = QLabel('OR')
        or_label.setAlignment(Qt.AlignCenter)
        or_layout.addWidget(or_label)
        or_layout.addWidget(self.create_line())
        right_layout.addLayout(or_layout)

        # Face Recognition Login Button
        face_login_button = QPushButton('Login with Face Recognition')
        face_login_button.clicked.connect(self.face_login)
        face_login_button.setStyleSheet("""
        QPushButton {
            color: #000000;
            background-color: #85def1;
            width: 200px;
            border: 1.5px solid black;
        }
        QPushButton:hover {
            background-color: #9de5f4;
        }""")
        right_layout.addWidget(face_login_button, alignment=Qt.AlignCenter)

        # Remember me and Forgot Password
        options_layout = QHBoxLayout()
        self.remember_me = QCheckBox("Remember me")
        options_layout.addWidget(self.remember_me)
        right_layout.addLayout(options_layout)
        main_layout.addWidget(right_widget)

        # Set the main widget as the central widget
        outer_layout = QVBoxLayout(self)
        outer_layout.addWidget(main_widget)
        self.setLayout(outer_layout)

        # Apply styles
        self.setStyleSheet("""
            QWidget {
                color: #000000;
                font-family: 'Arial', sans-serif;
            }
            QLineEdit {
                padding: 10px;
                border: 2px solid #000000;
                border-radius: 20px;
                background-color: #FFFFFF;
                color: #000000;
            }
            QPushButton {
                padding: 10px;
                background-color: #000000;
                color: #FFFF00;
                border: none;
                border-radius: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #333333;
            }
        """)

    def create_line(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #000000;")  # Set color and height
        return line

    def login(self):
        print("Invoked login method")
        # Implement your login logic here
        username = self.username_field.text()
        password = self.password_field.text()

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
            # Update the error message label and make it visible
            self.error_message.setText("Invalid login credentials. Please try again.")
            self.error_message.setVisible(True)

    def face_login(self):
        # This will trigger the face recognition process
        print("triggered face login")
        successful_login_userID = start_face_recognition(person_ref)

        # todo remove to ensure successful login is brought to main menu( for demo purpose )

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
        super().closeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
