import tkinter as tk
from tkinter import ttk
from .styles import apply_styles
from .profile_editor import ProfileEditor
from services.life_area import LifeAreaService
from services.mission import MissionService
from services.dragon import DragonService
from services.task import TaskService
from services.micro_habit import MicroHabitService


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
        self.notebook.pack(fill="both", expand=True)

        # Create tabs
        self.profile_frame = ttk.Frame(self.notebook)
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.life_areas_frame = ttk.Frame(self.notebook)
        self.missions_frame = ttk.Frame(self.notebook)
        self.habits_frame = ttk.Frame(self.notebook)
        self.tasks_frame = ttk.Frame(self.notebook)

        # Add tabs to notebook
        self.notebook.add(self.profile_frame, text="Profile")
        self.notebook.add(self.dashboard_frame, text="Dashboard")
        self.notebook.add(self.life_areas_frame, text="Life Areas")
        self.notebook.add(self.missions_frame, text="Missions")
        self.notebook.add(self.habits_frame, text="Habits")
        self.notebook.add(self.tasks_frame, text="Tasks")

        self.create_dashboard()
        self.create_profile()

    def create_dashboard(self):
        welcome_label = ttk.Label(
            self.dashboard_frame,
            text=f"Welcome to Phoenix, {self.name}!",
            font=("TkDefaultFont", 16, "bold"),
        )
        welcome_label.pack(pady=20)

        # Overall Progress
        progress_frame = ttk.LabelFrame(self.dashboard_frame, text="Overall Progress")
        progress_frame.pack(pady=10, padx=10, fill="x")

        overall_progress = self.progress_service.get_overall_progress(
            self.db_session, self.user_id
        )
        progress_bar = ttk.Progressbar(
            progress_frame, length=200, mode="determinate", value=overall_progress
        )
        progress_bar.pack(pady=10)
        ttk.Label(progress_frame, text=f"{overall_progress:.1f}%").pack()

        # Life Areas Summary
        life_areas_frame = ttk.LabelFrame(self.dashboard_frame, text="Life Areas")
        life_areas_frame.pack(pady=10, padx=10, fill="x")

        life_areas = self.life_area_service.get_user_life_areas(
            self.db_session, self.user_id
        )
        for area in life_areas[:5]:  # Show top 5 life areas
            area_progress = self.progress_service.get_life_area_progress(
                self.db_session, area.id
            )
            ttk.Label(life_areas_frame, text=f"{area.name}: {area_progress:.1f}%").pack(
                anchor="w"
            )

        # Active Missions
        missions_frame = ttk.LabelFrame(self.dashboard_frame, text="Active Missions")
        missions_frame.pack(pady=10, padx=10, fill="x")

        active_missions = self.mission_service.get_active_missions(
            self.db_session, self.user_id
        )
        for mission in active_missions[:3]:  # Show top 3 active missions
            ttk.Label(missions_frame, text=mission.name).pack(anchor="w")

        # Habits Streak
        habits_frame = ttk.LabelFrame(self.dashboard_frame, text="Habit Streaks")
        habits_frame.pack(pady=10, padx=10, fill="x")

        top_habits = self.micro_habit_service.get_top_streaks(
            self.db_session, self.user_id
        )
        for habit in top_habits[:3]:  # Show top 3 habit streaks
            ttk.Label(
                habits_frame, text=f"{habit.name}: {habit.current_streak} days"
            ).pack(anchor="w")

        # Motivational Quote (you can implement a quote service to get random quotes)
        quote_frame = ttk.LabelFrame(self.dashboard_frame, text="Daily Inspiration")
        quote_frame.pack(pady=10, padx=10, fill="x")
        ttk.Label(
            quote_frame,
            text="Your life does not get better by chance, it gets better by change.",
        ).pack(pady=5)

        # Quick Actions
        actions_frame = ttk.Frame(self.dashboard_frame)
        actions_frame.pack(pady=20)
        ttk.Button(
            actions_frame, text="Add New Mission", command=self.add_new_mission
        ).pack(side="left", padx=5)
        ttk.Button(actions_frame, text="Log Habit", command=self.log_habit).pack(
            side="left", padx=5
        )

    def create_profile(self):
        profile_frame = ttk.Frame(self.profile_frame, padding="20")
        profile_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            profile_frame,
            text=f"Profile of {self.user.name}",
            font=("TkDefaultFont", 16, "bold"),
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")

        labels = [
            "Name:",
            "Email:",
            "Life Mission:",
            "Heaven Scenario:",
            "Hell Scenario:",
            "Values:",
            "Current Focus:",
        ]
        values = [
            self.user.name,
            self.user.email,
            self.user.life_mission or "Add your life mission",
            self.user.heaven_scenario or "Add your heaven scenario",
            self.user.hell_scenario or "Add your hell scenario",
            self.user.values or "Add your values",
            self.user.current_focus or "Add your current focus",
        ]

        for i, (label, value) in enumerate(zip(labels, values)):
            ttk.Label(
                profile_frame, text=label, font=("TkDefaultFont", 11, "bold")
            ).grid(row=i + 1, column=0, pady=5, sticky="w")
            if label in [
                "Life Mission:",
                "Heaven Scenario:",
                "Hell Scenario:",
                "Values:",
                "Current Focus:",
            ]:
                text_widget = tk.Text(profile_frame, height=3, wrap=tk.WORD, width=40)
                text_widget.insert(tk.END, value)
                text_widget.config(state=tk.DISABLED)
                text_widget.grid(row=i + 1, column=1, pady=5, sticky="w")
            else:
                ttk.Label(profile_frame, text=value, wraplength=300).grid(
                    row=i + 1, column=1, pady=5, sticky="w"
                )

        edit_profile_button = ttk.Button(
            profile_frame, text="Edit Profile", command=self.open_profile_editor
        )
        edit_profile_button.grid(
            row=len(labels) + 1, column=0, columnspan=2, pady=(20, 0)
        )

        profile_frame.columnconfigure(1, weight=1)

    def open_profile_editor(self):
        ProfileEditor(
            self.master,
            self.user,
            self.user_service,
            self.db_session,
            self.refresh_profile,
        )

    def refresh_profile(self):
        # Refresh the user data
        self.user = self.user_service.get_user(self.db_session, self.user.id)

        # Clear and recreate the profile view
        for widget in self.profile_frame.winfo_children():
            widget.destroy()
        self.create_profile()
