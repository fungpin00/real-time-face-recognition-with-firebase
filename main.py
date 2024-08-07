import customtkinter as ctk
from PIL import Image, ImageTk
import cv2
import threading

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

class VideoWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("640x480")
        self.title("Face Recognition")

        self.video_label = ctk.CTkLabel(self,text="")
        self.video_label.pack(expand=True, fill="both")

        self.running = True
        self.video_capture = cv2.VideoCapture(0)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.update_frame()

    def update_frame(self):
        if self.running:
            ret, frame = self.video_capture.read()
            if ret:
                # Convert to grayscale for face detection
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Detect faces
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                # Draw rectangles around the faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                    # Add text to the top-left of the rectangle
                    text = "Face" #add logic where default is unauthorized, and when face is recognized then change
                    # to authroized, and change to font color as well
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 0.6
                    font_color = (255, 255, 255)  # White color for text
                    thickness = 2

                    # Position the text at the top-left corner of the rectangle
                    cv2.putText(frame, text, (x, y - 10), font, font_scale, font_color, thickness)

                # Convert frame to PhotoImage
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                photo = ImageTk.PhotoImage(image=image)

                self.video_label.configure(image=photo)
                self.video_label.image = photo

            self.after(10, self.update_frame)

    def on_closing(self):
        self.running = False
        if self.video_capture.isOpened():
            self.video_capture.release()
        self.destroy()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1024x768")
        self.title("Login")
        self.video_window = None

        # Create a frame for the login form
        self.login_frame = ctk.CTkFrame(master=self, width=650, height=600)
        self.login_frame.pack(pady=50, padx=50)
        self.login_frame.pack_propagate(False)

        self.theme_switch = ctk.CTkSwitch(master=self.login_frame, command=self.appearance_switch, text="Switch theme")
        self.theme_switch.pack(padx=100)

        self.username_label = ctk.CTkLabel(master=self.login_frame, text="Username", font=("Arial", 14))
        self.username_label.pack(pady=5, padx=20, anchor='center')
        self.username_entry = ctk.CTkEntry(master=self.login_frame, width=250, placeholder_text="Enter your username")
        self.username_entry.pack(pady=5)

        self.password_label = ctk.CTkLabel(master=self.login_frame, text="Password", font=("Arial", 14))
        self.password_label.pack(pady=5, padx=20, anchor='center')
        self.password_entry = ctk.CTkEntry(master=self.login_frame, width=250, placeholder_text="Enter your password", show="*")
        self.password_entry.pack(pady=5)

        self.button_frame = ctk.CTkFrame(master=self.login_frame)
        self.button_frame.pack(pady=10)

        self.login_button = ctk.CTkButton(master=self.button_frame, text="Login", width=120)
        self.login_button.pack(side="left", padx=8)

        self.face_icon = ctk.CTkImage(Image.open("images/1231006.png"))
        self.face_reg = ctk.CTkButton(master=self.button_frame, image=self.face_icon, text="", width=120, command=self.open_video_window)
        self.face_reg.pack(side="left", padx=8)

    def appearance_switch(self):
        current_appearance = ctk.get_appearance_mode()
        if current_appearance == "dark":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")

    def open_video_window(self):
        if self.video_window is None or not self.video_window.winfo_exists():
            self.video_window = VideoWindow(self)
            self.video_window.focus()
        else:
            self.video_window.focus()

if __name__ == "__main__":
    app = App()
    app.mainloop()