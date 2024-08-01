import tkinter as tk
from tkinter import messagebox

# Create the main application window
root = tk.Tk()
root.title("Login Form")
root.geometry("400x300")

# Username Label and Entry
username_label = tk.Label(root, text="Username", font=("Arial", 14))
username_label.pack(pady=10)
username_entry = tk.Entry(root, font=("Arial", 14))
username_entry.pack(pady=5)

# Password Label and Entry
password_label = tk.Label(root, text="Password", font=("Arial", 14))
password_label.pack(pady=10)
password_entry = tk.Entry(root, font=("Arial", 14), show="*")
password_entry.pack(pady=5)

# Login Button
def login():
    username = username_entry.get()
    password = password_entry.get()

    # Here you would typically check the username and password
    if username == "admin" and password == "password":  # Replace with real authentication logic
        messagebox.showinfo("Login", "Login successful!")
    else:
        messagebox.showerror("Login", "Invalid username or password")

login_button = tk.Button(root, text="Login", command=login, font=("Arial", 14))
login_button.pack(pady=20)

# Run the application
root.mainloop()
