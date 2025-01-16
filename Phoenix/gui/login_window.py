import tkinter as tk
from tkinter import ttk, messagebox
from services.user import UserService
from schemas.user import UserCreate
from .styles import apply_styles
from models.database import SessionLocal

class LoginWindow:
    def __init__(self, master, on_user_selected):
        self.master = master
        self.on_user_selected = on_user_selected
        self.user_service = UserService()
        self.db = SessionLocal()
        apply_styles()
        self.create_widgets()

    def create_widgets(self):
        self.frame = ttk.Frame(self.master, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.frame, text="Select a user:").pack(pady=10)

        self.user_listbox = tk.Listbox(self.frame, width=50)
        self.user_listbox.pack(pady=10, padx=10)

        self.refresh_user_list()

        ttk.Button(self.frame, text="Login", command=self.login).pack(pady=5)
        ttk.Button(self.frame, text="Create New User", command=self.open_create_user_window).pack(pady=10)

    def refresh_user_list(self):
        self.user_listbox.delete(0, tk.END)
        users = self.user_service.get_users(self.db)
        for user in users:
            self.user_listbox.insert(tk.END, f"{user.name} ({user.email})")

    def login(self):
        selection = self.user_listbox.curselection()
        if selection:
            index = selection[0]
            user = self.user_service.get_users(self.db)[index]
            self.on_user_selected(user)
        else:
            messagebox.showerror("Error", "Please select a user")

    def open_create_user_window(self):
        create_window = tk.Toplevel(self.master, padx=20, pady=10)
        create_window.title("Create New User")

        ttk.Label(create_window, text="Name:").pack(pady=5)
        name_entry = ttk.Entry(create_window)
        name_entry.pack(pady=5)

        ttk.Label(create_window, text="Email:").pack(pady=5)
        email_entry = ttk.Entry(create_window)
        email_entry.pack(pady=5)

        def create_user():
            name = name_entry.get()
            email = email_entry.get()
            if name and email:
                user_create = UserCreate(name=name, email=email)
                self.user_service.create_user(self.db, user_create)
                self.refresh_user_list()
                create_window.destroy()
            else:
                messagebox.showerror("Error", "Please fill in all fields")

        ttk.Button(create_window, text="Create", command=create_user).pack(pady=10)

    def __del__(self):
        if hasattr(self, 'db'):
            self.db.close()