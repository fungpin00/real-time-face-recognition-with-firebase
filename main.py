import customtkinter as ctk
from PIL import Image

from src.face_detection import open_video


def appearance_switch():
    current_appearance = ctk.get_appearance_mode()
    if current_appearance == "dark":
        ctk.set_appearance_mode("light")
    else:
        ctk.set_appearance_mode("dark")

# Initialize the main window
app = ctk.CTk()
app.geometry("1024x768")
app.title("Login")

# Create a frame for the login form
login_frame = ctk.CTkFrame(master=app, width=650, height=600)
login_frame.pack(pady=50, padx=50)  # Center the frame with margin

login_frame.pack_propagate(False)

theme_switch = ctk.CTkSwitch(master=login_frame,command=appearance_switch(),text="Switch theme")
theme_switch.pack(padx=100)

title_label = ctk.CTkLabel(master=login_frame, text="Login", font=("Arial", 24))
title_label.pack(pady=80)

username_label = ctk.CTkLabel(master=login_frame, text="Username", font=("Arial", 14))
username_label.pack(pady=10, padx=20, anchor='center')
username_entry = ctk.CTkEntry(master=login_frame, width=250, placeholder_text="Enter your username")
username_entry.pack(pady=10)

password_label = ctk.CTkLabel(master=login_frame, text="Password", font=("Arial", 14))
password_label.pack(pady=10, padx=20, anchor='center')
password_entry = ctk.CTkEntry(master=login_frame, width=250, placeholder_text="Enter your password", show="*")
password_entry.pack(pady=10)

button_frame = ctk.CTkFrame(master=login_frame)
button_frame.pack(pady=20)

login_button = ctk.CTkButton(master=button_frame, text="Login", width=120)
login_button.pack(side="left", padx=8)

face_icon = ctk.CTkImage(Image.open("images/1231006.png"))
face_reg = ctk.CTkButton(master=button_frame, image=face_icon, text="", width=120, command=open_video())
face_reg.pack(side="left", padx=8)


# Center the content inside the frame

# Run the application
app.mainloop()
