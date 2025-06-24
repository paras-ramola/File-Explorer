import os
import platform
import subprocess
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import sys
from datetime import datetime

HOME = os.path.expanduser("~")

SYSTEM_FOLDERS = {
    "Root": os.path.abspath(os.sep),
    "Home": HOME,
    "Desktop": os.path.join(HOME, "Desktop"),
    "Documents": os.path.join(HOME, "Documents"),
    "Downloads": os.path.join(HOME, "Downloads"),
    "Pictures": os.path.join(HOME, "Pictures"),
}

class FileExplorer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NAVI EXPLORER")
        self.geometry("900x650")
        self.configure(bg="#2c3e50") 

        self.folder_icon = ImageTk.PhotoImage(Image.open("images/folder_icon.png").resize((48, 48)))
        self.document_icon = ImageTk.PhotoImage(Image.open("images/file_icon.png").resize((48, 48)))
        self.application_icon = ImageTk.PhotoImage(Image.open("images/app_icon.png").resize((48, 48)))
        self.unknown_icon = ImageTk.PhotoImage(Image.open("images/folder_icon.png").resize((48, 48)))

        self.current_path = None
        self.all_items = []  
        self.clipboard = None  
        self.current_sort = "name" 
        self.sort_reverse = False  # sort direction

        self.history = [] 
        self.recent_files = [] 

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

    def open_Cli(self):
        try:
            system = platform.system()
            if system == "Windows":
                subprocess.Popen(["wsl", "xterm", "-fa", "fixed", "-fs", "12", "-e", "cli_explorer.c"])
            elif system == "Linux":
                subprocess.Popen(["xterm", "-fa", "Monospace", "-fs", "12", "-e", "cli_explorer.c"])
            elif system == "Darwin":
                script = f"""
                tell application "Terminal"
                    do script "cd '{os.getcwd()}' && ./explorer"
                    activate
                end tell
                """
                subprocess.run(["osascript", "-e", script])
            else:
                messagebox.showerror("Unsupported OS", f"Your OS ({system}) is not supported.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open CLI explorer.\n{e}")

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

        # Sorting Section
        sort_label = tk.Label(sidebar, text="Sort By", bg="#34495e", fg="white",
                              font=("Segoe UI", 12, "bold"))
        sort_label.pack(pady=(20, 5))

        # Sort buttons
        sort_buttons = [
            ("Name", "name"),
            ("Date", "date"),
            ("Size", "size"),
            ("Type", "type")
        ]

        for text, sort_type in sort_buttons:
            btn = tk.Button(
                sidebar,
                text=text,
                fg="black",
                bg="#4a6d8c",
                activebackground="#3d566e",
                activeforeground="white",
                bd=0,
                font=("Segoe UI", 10, "bold"),
                cursor="hand2",
                command=lambda st=sort_type: self.sort_files(st)
            )
            btn.pack(fill="x", pady=2, padx=10)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#3d566e"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#4a6d8c"))

        # Recent files button
        recent_btn = tk.Button(
            sidebar,
            text="Recent Files",
            fg="black",
            bg="#5a6c7d",
            activebackground="#4a5c6d",
            activeforeground="white",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            command=self.show_recent_files
        )
        recent_btn.pack(fill="x", pady=2, padx=10)
        recent_btn.bind("<Enter>", lambda e: recent_btn.config(bg="#4a5c6d"))
        recent_btn.bind("<Leave>", lambda e: recent_btn.config(bg="#5a6c7d"))

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

        # Command Line Interface section
        cli_label = tk.Label(sidebar, text="Command Line Interface", bg="#34495e", fg="white",
                             font=("Segoe UI", 12, "bold"))
        cli_label.pack(pady=(20, 5))

        cli_btn = tk.Button(
            sidebar,
            text="Open Terminal",
            fg="black",
            bg="#4a6d8c",
            activebackground="#3d566e",
            activeforeground="white",
            bd=0,
            font=("Segoe UI", 14, "bold"),
            cursor="hand2",
            command=self.open_Cli
        )
        cli_btn.pack(fill="x", pady=5, padx=10)
        cli_btn.bind("<Enter>", lambda e: cli_btn.config(bg="#3d566e"))
        cli_btn.bind("<Leave>", lambda e: cli_btn.config(bg="#4a6d8c"))
        
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
        back_login_btn.pack(fill="x", pady=15, padx=15)
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

    def sort_files(self, sort_type):
        """Sort files based on the selected criteria"""
        if self.current_sort == sort_type:
       
            self.sort_reverse = not self.sort_reverse
        else:
            self.current_sort = sort_type
            self.sort_reverse = False

        if not self.all_items:
            return

        try:
            if sort_type == "name":
                sorted_items = sorted(self.all_items, 
                                    key=lambda x: (not os.path.isdir(x[1]), x[0].lower()),
                                    reverse=self.sort_reverse)
            elif sort_type == "date":
                sorted_items = sorted(self.all_items,
                                    key=lambda x: (not os.path.isdir(x[1]), 
                                                 os.path.getmtime(x[1]) if os.path.exists(x[1]) else 0),
                                    reverse=not self.sort_reverse)  # Most recent first by default
            elif sort_type == "size":
                def get_size(path):
                    if os.path.isdir(path):
                        return 0  # Directories come first
                    try:
                        return os.path.getsize(path)
                    except:
                        return 0
                
                sorted_items = sorted(self.all_items,
                                    key=lambda x: (not os.path.isdir(x[1]), get_size(x[1])),
                                    reverse=self.sort_reverse)
            elif sort_type == "type":
                def get_extension(path):
                    if os.path.isdir(path):
                        return "" 
                    return os.path.splitext(path)[1].lower()
                
                sorted_items = sorted(self.all_items,
                                    key=lambda x: (not os.path.isdir(x[1]), get_extension(x[1])),
                                    reverse=self.sort_reverse)
            else:
                sorted_items = self.all_items

            # Clear previous content
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()

            self.display_items(sorted_items)
            
        except Exception as e:
            messagebox.showerror("Sort Error", f"Error sorting files: {e}")

    def show_recent_files(self):
        """Display recently accessed files"""
        if not self.recent_files:
            messagebox.showinfo("Recent Files", "No recent files to display.")
            return
        
        # Create a new window to show recent files
        recent_window = tk.Toplevel(self)
        recent_window.title("Recent Files")
        recent_window.geometry("500x400")
        recent_window.configure(bg="#2c3e50")
        
        # Create listbox for recent files
        listbox_frame = tk.Frame(recent_window, bg="#2c3e50")
        listbox_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side="right", fill="y")
        
        listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set,
                           bg="#34495e", fg="white", font=("Segoe UI", 10))
        listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=listbox.yview)
        

        for file_path in reversed(self.recent_files):
            if os.path.exists(file_path):
                file_name = os.path.basename(file_path)
                listbox.insert(tk.END, f"{file_name} - {file_path}")
        
        def open_selected_file():
            selection = listbox.curselection()
            if selection:
                selected_text = listbox.get(selection[0])
                file_path = selected_text.split(" - ", 1)[1]
                if os.path.exists(file_path):
                    self.open_file(file_path)
                    recent_window.destroy()
        
   
        open_btn = tk.Button(recent_window, text="Open Selected", 
                           command=open_selected_file,
                           bg="#4a6d8c", fg="white", font=("Segoe UI", 10, "bold"))
        open_btn.pack(pady=5)
        

        listbox.bind('<Double-1>', lambda e: open_selected_file())

    def add_to_recent_files(self, file_path):
        """Add a file to the recent files list"""
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)
        self.recent_files.append(file_path)
        
       
        if len(self.recent_files) > 20:
            self.recent_files.pop(0)

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

  
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        try:
            items = os.listdir(path)
        except PermissionError:
            messagebox.showerror("Error", f"Permission denied:\n{path}")
            return

        self.all_items = [(item, os.path.join(path, item)) for item in items]

        # Apply current sorting
        self.sort_files(self.current_sort)

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
        menu.add_command(label="Rename", command=lambda: self.rename_path(path))
        menu.add_command(label="Copy", command=lambda: self.copy_path(path))
        if is_dir:
            menu.add_command(label="Delete Folder", command=lambda: self.delete_folder(path))
        else:
            menu.add_command(label="Delete File", command=lambda: self.delete_file(path))
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def open_path(self, path, is_dir):
        if is_dir:
            self.load_folder(path)
        else:
            self.open_file(path)
            
            self.add_to_recent_files(path)

    def rename_path(self, old_path):
        old_name = os.path.basename(old_path)
        new_name = simpledialog.askstring("Rename", f"Enter new name for:\n{old_name}", parent=self)
        if new_name:
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            if os.path.exists(new_path):
                messagebox.showerror("Error", "A file or folder with that name already exists.")
                return
            try:
                os.rename(old_path, new_path)
                self.load_folder(self.current_path)
            except Exception as e:
                messagebox.showerror("Error", f"Could not rename:\n{e}")

    def copy_path(self, path):
        self.clipboard = path
        messagebox.showinfo("Copied", f"Copied to clipboard:\n{os.path.basename(path)}")

    def delete_folder(self, path):
        confirm = messagebox.askyesno("Delete Folder", f"Are you sure you want to permanently delete the folder?\n{path}")
        if confirm:
            try:
                shutil.rmtree(path)
                self.load_folder(self.current_path)
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete folder:\n{e}")

    def delete_file(self, path):
        confirm = messagebox.askyesno("Delete File", f"Are you sure you want to permanently delete the file?\n{path}")
        if confirm:
            try:
                os.remove(path)
                self.load_folder(self.current_path)
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete file:\n{e}")

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