import os
import platform
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import sys

# Define home directory
HOME = os.path.expanduser("~")

# System folders including root and home for quick access
SYSTEM_FOLDERS = {
    "Desktop": os.path.join(HOME, "Desktop"),
    "Documents": os.path.join(HOME, "Documents"),
    "Downloads": os.path.join(HOME, "Downloads"),
    "Pictures": os.path.join(HOME, "Pictures"),
}

class FileExplorer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NAVI EXPLORER")
        self.geometry("900x600")
        self.configure(bg="#2c3e50")  

  
        self.folder_icon = ImageTk.PhotoImage(Image.open("images/folder_icon.png").resize((48, 48)))
        self.document_icon = ImageTk.PhotoImage(Image.open("images/file_icon.png").resize((48, 48)))
        self.application_icon = ImageTk.PhotoImage(Image.open("images/app_icon.png").resize((48, 48)))
        self.unknown_icon = ImageTk.PhotoImage(Image.open("images/folder_icon.png").resize((48, 48)))

        self.current_path = None
        self.all_items = [] 
        self.clipboard = None  

        self.history = []

        self.setup_ui()

        start_path = os.path.join(HOME, "Desktop")
        if not os.path.exists(start_path):
            start_path = HOME
        self.load_folder(start_path)

    def get_icon_for_file(self, filename, is_dir):
        if is_dir:
            return self.folder_icon
        ext = os.path.splitext(filename)[1].lower()
        if ext in [".txt", ".pdf", ".doc", ".docx", ".odt"]:
            return self.document_icon
        elif ext in [".exe", ".app", ".sh", ".bat", ".webloc"]:
            return self.application_icon
        else:
            return self.unknown_icon



    def setup_ui(self):
        # Sidebar for system folders + CLI section and new create file/folder section
        sidebar = tk.Frame(self, bg="#34495e", width=220)
        sidebar.pack(side="left", fill="y")

        # Search bar
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(sidebar, textvariable=self.search_var, font=("Segoe UI", 12),
                                bg="#2c3e50", fg="white", insertbackground="white")
        search_entry.pack(pady=10, padx=10, fill="x")
        search_entry.bind("<KeyRelease>", self.search_files)

        # Back button
        back_btn = tk.Button(
            sidebar,
            text="⬅ Back",
            fg="black",
            bg="#4a6d8c",
            activebackground="#3d566e",
            activeforeground="white",
            bd=0,
            font=("Segoe UI", 14, "bold"),
            cursor="hand2",
            command=self.go_back
        )
        back_btn.pack(fill="x", pady=5, padx=10)
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg="#3d566e"))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg="#4a6d8c"))

        # System folders section
        self.create_folder_buttons(sidebar, SYSTEM_FOLDERS, "System")

        # Create New File/Folder Section
        create_label = tk.Label(sidebar, text="Create New", bg="#34495e", fg="white",
                                font=("Segoe UI", 12, "bold"))
        create_label.pack(pady=(20, 5))

        # New folder entry and button
        self.new_folder_var = tk.StringVar()
        folder_entry = ttk.Entry(sidebar, width=25, textvariable=self.new_folder_var)
        folder_entry.pack(padx=10, pady=(5, 2), fill="x")

        create_folder_btn = tk.Button(
            sidebar,
            text="New Folder",
            fg="black",
            bg="#4a6d8c",
            activebackground="#3d566e",
            activeforeground="white",
            bd=0,
            font=("Segoe UI", 12, "bold"),
            cursor="hand2",
            command=self.create_new_folder
        )
        create_folder_btn.pack(pady=(0, 10), padx=10, fill="x")
        create_folder_btn.bind("<Enter>", lambda e: create_folder_btn.config(bg="#3d566e"))
        create_folder_btn.bind("<Leave>", lambda e: create_folder_btn.config(bg="#4a6d8c"))

        # New file entry and button
        self.new_file_var = tk.StringVar()
        file_entry = ttk.Entry(sidebar, width=25, textvariable=self.new_file_var)
        file_entry.pack(padx=10, pady=(5, 2), fill="x")

        create_file_btn = tk.Button(
            sidebar,
            text="New File",
            fg="black",
            bg="#4a6d8c",
            activebackground="#3d566e",
            activeforeground="white",
            bd=0,
            font=("Segoe UI", 12, "bold"),
            cursor="hand2",
            command=self.create_new_file
        )
        create_file_btn.pack(pady=(0, 10), padx=10, fill="x")
        create_file_btn.bind("<Enter>", lambda e: create_file_btn.config(bg="#3d566e"))
        create_file_btn.bind("<Leave>", lambda e: create_file_btn.config(bg="#4a6d8c"))

    
        back_login_btn = tk.Button(
            sidebar,
            text="Back to Login",
             fg="black",
             bg="#e74c3c",
            activebackground="#c0392b",
            activeforeground="white",
            bd=0,
            font=("Segoe UI", 12, "bold"),
            cursor="hand2",
            command=self.back_to_login
            )
        back_login_btn.pack(fill="x", pady=10, padx=10)
        back_login_btn.bind("<Enter>", lambda e: back_login_btn.config(bg="#c0392b"))
        back_login_btn.bind("<Leave>", lambda e: back_login_btn.config(bg="#e74c3c"))

        # Main content frame with scrollable canvas
        self.main_frame = tk.Frame(self, bg="#2c3e50")
        self.main_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.main_frame, bg="#2c3e50", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#2c3e50")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Current path label
        self.path_label = tk.Label(
            self,
            text="",
            bg="#34495e",
            fg="white",
            font=("Segoe UI", 11, "italic"),
            anchor="w",
            padx=10,
            pady=5,
        )
        self.path_label.pack(side="bottom", fill="x")
        
        

    def go_back(self):
        if self.history:
            previous_path = self.history.pop()
            self.load_folder(previous_path, add_history=False)
            
    def back_to_login(self):
         subprocess.Popen([sys.executable, "front.py"])
         self.destroy()


    def create_folder_buttons(self, parent, folder_dict, section_title):
        title_label = tk.Label(parent, text=section_title, bg="#34495e", fg="white",
                               font=("Segoe UI", 12, "bold"))
        title_label.pack(pady=(10, 0))

        for name, path in folder_dict.items():
            btn = tk.Button(
                parent,
                text=name,
                fg="black",
                bg="#34495e",
                activebackground="#3d566e",
                activeforeground="white",
                bd=0,
                font=("Segoe UI", 14, "bold"),
                command=lambda p=path: self.load_folder(p),
                cursor="hand2",
            )
            btn.pack(fill="x", pady=5, padx=10)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#3d566e"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#34495e"))

    def load_folder(self, path, add_history=True):
        if not os.path.exists(path):
            messagebox.showerror("Error", f"Folder does not exist:\n{path}")
            return

        if self.current_path and add_history and self.current_path != path:
            self.history.append(self.current_path)

        self.current_path = path
        self.path_label.config(text=f"Current path: {path}")

        # Clear previous content
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        try:
            items = os.listdir(path)
        except PermissionError:
            messagebox.showerror("Error", f"Permission denied:\n{path}")
            return

        items.sort(key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower()))

        self.all_items = [(item, os.path.join(path, item)) for item in items]

        self.display_items(self.all_items)

    def display_items(self, items):
        columns = 4
        for index, (item, abs_path) in enumerate(items):
            is_dir = os.path.isdir(abs_path)

            icon = self.get_icon_for_file(item, is_dir)

            frame = tk.Frame(self.scrollable_frame, bg="#2c3e50", padx=10, pady=10)
            frame.grid(row=index // columns, column=index % columns, sticky="nw")

            btn = tk.Button(
                frame,
                image=icon,
                bd=0,
                bg="#2c3e50",
                activebackground="#34495e",
                cursor="hand2",
            )
            btn.image = icon  
            btn.pack()
            frame.bind("<Button-1>", lambda e, p=abs_path, isd=is_dir: self.show_options_menu(e, p, isd))
            btn.bind("<Button-1>", lambda e, p=abs_path, isd=is_dir: self.show_options_menu(e, p, isd))

            label = tk.Label(
                frame,
                text=item,
                bg="#2c3e50",
                fg="white",
                wraplength=120,
                justify="center",
                font=("Segoe UI", 10),
            )
            label.pack()
            label.bind("<Button-1>", lambda e, p=abs_path, isd=is_dir: self.show_options_menu(e, p, isd))

    def show_options_menu(self, event, path, is_dir):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Open", command=lambda: self.open_path(path, is_dir))
        menu.add_command(label="Copy", command=lambda: self.copy_path(path))
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def open_path(self, path, is_dir):
        if is_dir:
            self.load_folder(path)
        else:
            self.open_file(path)


    def copy_path(self, path):
        self.clipboard = path
        messagebox.showinfo("Copied", f"Copied to clipboard:\n{os.path.basename(path)}")


    def search_files(self, event=None):
        query = self.search_var.get().lower()
        if not self.all_items:
            return

        filtered_items = [item for item in self.all_items if query in item[0].lower()]

        # Clear previous content
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.display_items(filtered_items)

    def open_file(self, filepath):
        try:
            if platform.system() == "Windows":
                os.startfile(filepath)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", filepath])
            else:
                subprocess.Popen(["xdg-open", filepath])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file:\n{e}")

    def create_new_folder(self):
        folder_name = self.new_folder_var.get().strip()
        if not folder_name:
            messagebox.showwarning("Input Error", "Please enter a folder name.")
            return
        if not self.current_path:
            messagebox.showwarning("Error", "No current directory selected.")
            return
        new_folder_path = os.path.join(self.current_path, folder_name)
        if os.path.exists(new_folder_path):
            messagebox.showwarning("Exists", f"Folder '{folder_name}' already exists.")
            return
        try:
            os.makedirs(new_folder_path)
            messagebox.showinfo("Success", f"Folder '{folder_name}' created successfully in current directory.")
            self.new_folder_var.set("")
            self.load_folder(self.current_path, add_history=False)
        except Exception as e:
            messagebox.showerror("Error", f"Could not create folder:\n{e}")

    def create_new_file(self):
        file_name = self.new_file_var.get().strip()
        if not file_name:
            messagebox.showwarning("Input Error", "Please enter a file name.")
            return
        if not self.current_path:
            messagebox.showwarning("Error", "No current directory selected.")
            return
        new_file_path = os.path.join(self.current_path, file_name)
        if os.path.exists(new_file_path):
            messagebox.showwarning("Exists", f"File '{file_name}' already exists.")
            return
        try:
            with open(new_file_path, 'w') as f:
                pass
            messagebox.showinfo("Success", f"File '{file_name}' created successfully in current directory.")
            self.new_file_var.set("")
            self.load_folder(self.current_path, add_history=False)
        except Exception as e:
            messagebox.showerror("Error", f"Could not create file:\n{e}")

if __name__ == "__main__":
    app = FileExplorer()
    app.mainloop()
