import tkinter as tk
from tkinter import ttk, messagebox
from schemas.user import UserUpdate

class ProfileEditor:
    def __init__(self, master, user, user_service, db_session, refresh_callback):
        self.user = user
        self.user_service = user_service
        self.db_session = db_session
        self.refresh_callback = refresh_callback

        self.window = tk.Toplevel(master)
        self.window.title("Edit Profile")
        self.window.geometry("400x500")

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Name
        ttk.Label(main_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(main_frame)
        self.name_entry.insert(0, self.user.name)
        self.name_entry.grid(row=0, column=1, sticky=tk.EW, pady=5)

        # Email
        ttk.Label(main_frame, text="Email:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.email_entry = ttk.Entry(main_frame)
        self.email_entry.insert(0, self.user.email)
        self.email_entry.grid(row=1, column=1, sticky=tk.EW, pady=5)

        # Life Mission
        ttk.Label(main_frame, text="Life Mission:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.life_mission_text = tk.Text(main_frame, height=3, wrap=tk.WORD)
        self.life_mission_text.insert(tk.END, self.user.life_mission or "")
        self.life_mission_text.grid(row=2, column=1, sticky=tk.EW, pady=5)

        # Heaven Scenario
        ttk.Label(main_frame, text="Heaven Scenario:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.heaven_scenario_text = tk.Text(main_frame, height=3, wrap=tk.WORD)
        self.heaven_scenario_text.insert(tk.END, self.user.heaven_scenario or "")
        self.heaven_scenario_text.grid(row=3, column=1, sticky=tk.EW, pady=5)

        # Hell Scenario
        ttk.Label(main_frame, text="Hell Scenario:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.hell_scenario_text = tk.Text(main_frame, height=3, wrap=tk.WORD)
        self.hell_scenario_text.insert(tk.END, self.user.hell_scenario or "")
        self.hell_scenario_text.grid(row=4, column=1, sticky=tk.EW, pady=5)

        # Values
        ttk.Label(main_frame, text="Values:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.values_text = tk.Text(main_frame, height=3, wrap=tk.WORD)
        self.values_text.insert(tk.END, self.user.values or "")
        self.values_text.grid(row=5, column=1, sticky=tk.EW, pady=5)

        # Current Focus
        ttk.Label(main_frame, text="Current Focus:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.current_focus_entry = ttk.Entry(main_frame)
        self.current_focus_entry.insert(0, self.user.current_focus or "")
        self.current_focus_entry.grid(row=6, column=1, sticky=tk.EW, pady=5)

        # Save Button
        save_button = ttk.Button(main_frame, text="Save Changes", command=self.save_changes)
        save_button.grid(row=7, column=0, columnspan=2, pady=20)

        # Configure grid
        main_frame.columnconfigure(1, weight=1)

    def save_changes(self):
        updated_user = UserUpdate(
            name=self.name_entry.get(),
            email=self.email_entry.get(),
            life_mission=self.life_mission_text.get("1.0", tk.END).strip(),
            heaven_scenario=self.heaven_scenario_text.get("1.0", tk.END).strip(),
            hell_scenario=self.hell_scenario_text.get("1.0", tk.END).strip(),
            values=self.values_text.get("1.0", tk.END).strip(),
            current_focus=self.current_focus_entry.get(),
        )
        self.user_service.update_user(self.db_session, self.user.id, updated_user)
        messagebox.showinfo("Success", "Profile updated successfully!")
        self.refresh_callback()
        self.window.destroy()