import tkinter as tk
from tkinter import ttk 
from .styles import apply_styles
from .profile_editor import ProfileEditor

class MainWindow:
    def __init__(self, master, name, user_service, db_session, user_id):
        self.master = master
        self.name = name
        self.user_service = user_service
        self.db_session = db_session
        self.user_id = user_id
        self.user = self.user_service.get_user(self.db_session, self.user_id)
        apply_styles()

        self.create_widgets()

    def create_widgets(self):
        # Notebooks are for grouping related widgets such that the user can navigate through them easily
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill='both', expand=True)

        # Create tabs
        self.profile_frame = ttk.Frame(self.notebook)
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.life_areas_frame = ttk.Frame(self.notebook)
        self.missions_frame = ttk.Frame(self.notebook)
        self.habits_frame = ttk.Frame(self.notebook)

        # Add tabs to notebook
        self.notebook.add(self.profile_frame, text='Profile')
        self.notebook.add(self.dashboard_frame, text='Dashboard')
        self.notebook.add(self.life_areas_frame, text='Life Areas')
        self.notebook.add(self.missions_frame, text='Missions')
        self.notebook.add(self.habits_frame, text='Habits')

        self.create_dashboard()
        self.create_profile()

    def create_dashboard(self):
        welcome_label = ttk.Label(self.dashboard_frame, text=f'Welcome to Phoenix, {self.name}!')
        welcome_label.pack(pady=20)

        # Add more dashboard widgets here
        overview_label = ttk.Label(self.dashboard_frame, text="Your Progress Overview")
        overview_label.pack(pady=10)

        # Placeholder for progress bars or other visualizations
        progress_frame = ttk.Frame(self.dashboard_frame)
        progress_frame.pack(pady=10)

        # Example progress bar (you can replace this with actual user data)
        progress_bar = ttk.Progressbar(progress_frame, length=200, mode='determinate', value=50)
        progress_bar.pack()

        # Add more dashboard elements as needed
    def create_profile(self):
        profile_frame = ttk.Frame(self.profile_frame, padding="20")
        profile_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(profile_frame, text=f"Profile of {self.user.name}", font=("TkDefaultFont", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")

        labels = ["Name:", "Email:", "Life Mission:", "Heaven Scenario:", "Hell Scenario:", "Values:", "Current Focus:"]
        values = [
            self.user.name,
            self.user.email,
            self.user.life_mission or "Add your life mission",
            self.user.heaven_scenario or "Add your heaven scenario",
            self.user.hell_scenario or "Add your hell scenario",
            self.user.values or "Add your values",
            self.user.current_focus or "Add your current focus"
        ]

        for i, (label, value) in enumerate(zip(labels, values)):
            ttk.Label(profile_frame, text=label, font=("TkDefaultFont", 11, "bold")).grid(row=i+1, column=0, pady=5, sticky="w")
            if label in ["Life Mission:", "Heaven Scenario:", "Hell Scenario:", "Values:", "Current Focus:"]:
                text_widget = tk.Text(profile_frame, height=3, wrap=tk.WORD, width=40)
                text_widget.insert(tk.END, value)
                text_widget.config(state=tk.DISABLED)
                text_widget.grid(row=i+1, column=1, pady=5, sticky="w")
            else:
                ttk.Label(profile_frame, text=value, wraplength=300).grid(row=i+1, column=1, pady=5, sticky="w")

        edit_profile_button = ttk.Button(profile_frame, text="Edit Profile", command=self.open_profile_editor)
        edit_profile_button.grid(row=len(labels)+1, column=0, columnspan=2, pady=(20, 0))

        profile_frame.columnconfigure(1, weight=1)

    def open_profile_editor(self):
        ProfileEditor(self.master, self.user, self.user_service, self.db_session, self.refresh_profile)

    def refresh_profile(self):
        # Refresh the user data
        self.user = self.user_service.get_user(self.db_session, self.user.id)
        
        # Clear and recreate the profile view
        for widget in self.profile_frame.winfo_children():
            widget.destroy()
        self.create_profile()