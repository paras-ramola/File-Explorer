import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import sys


def open_guest_page():
    subprocess.Popen([sys.executable, "guest.py"])
    root.destroy()

def verify_admin(pswrd):
    if pswrd == "1234":
        subprocess.Popen([sys.executable, "admin.py"])
        root.destroy()
    else:
        messagebox.showwarning("Wrong Password", "Please enter a correct password")

def toggle_password():
    if password_entry.cget('show') == '':
        password_entry.config(show='*')
        toggle_btn.config(text='Show')
    else:
        password_entry.config(show='')
        toggle_btn.config(text='Hide')

def show_password_frame():
    password_frame.pack(pady=20)

def submit_password():
    verify_admin(password_var.get())

# ==================== Main Window ====================
root = tk.Tk()
root.title("NAVI EXPLORER")
root.geometry("700x550")
root.configure(bg="#2e2e2e")


style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Segoe UI", 12), padding=6, background="#007acc", foreground="white")
style.configure("TLabel", background="#2e2e2e", foreground="white", font=("Segoe UI", 14))
style.configure("TEntry", padding=5)


tk.Label(root, text="Welcome to Navi Explorer", bg="#2e2e2e", fg="white", font=("Segoe UI", 24, "bold")).pack(pady=20)


img_raw = Image.open("images/blank_dp.jpg").resize((300, 200))
img = ImageTk.PhotoImage(img_raw)
tk.Label(root, image=img, bg="#2e2e2e").pack(pady=10)


btn_frame = tk.Frame(root, bg="#2e2e2e")
btn_frame.pack(pady=10)

ttk.Button(btn_frame, text="Guest", command=open_guest_page).grid(row=0, column=0, padx=20)
ttk.Button(btn_frame, text="Administrator", command=show_password_frame).grid(row=0, column=1, padx=20)

# ==================== Password Frame ====================
password_frame = tk.Frame(root, bg="#2e2e2e")

ttk.Label(password_frame, text="Enter Admin Password:").grid(row=0, column=0, sticky="w", pady=(10, 5))

password_var = tk.StringVar()
password_entry = ttk.Entry(password_frame, width=30, textvariable=password_var, show="*")
password_entry.grid(row=1, column=0, pady=5, sticky="w")

toggle_btn = ttk.Button(password_frame, text="Show", width=6, command=toggle_password)
toggle_btn.grid(row=1, column=1, padx=10)

ttk.Button(password_frame, text="Submit", command=submit_password).grid(row=2, column=0, columnspan=2, pady=15)


root.mainloop()
