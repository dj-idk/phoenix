import tkinter as tk
from models.database import engine, SessionLocal
from models import Base
from gui.login_window import LoginWindow
from gui.main_window import MainWindow
from services.user import UserService

def main():
    # Create database tables
    Base.metadata.create_all(bind=engine)

    root = tk.Tk()
    root.title("Phoenix - Rise from the Ashes")
    root.geometry("400x400")

    user_service = UserService()
    db_session = SessionLocal()

    def on_user_selected(user):
        root.withdraw()  # Hide the login window
        main_window = tk.Toplevel()
        main_window.title("Phoenix - Rise from the Ashes")
        main_window.geometry("800x600")
        app = MainWindow(main_window, user.name, user_service, db_session, user.id)

        def on_main_window_close():
            main_window.destroy()
            root.deiconify()  # Show the login window again

        main_window.protocol("WM_DELETE_WINDOW", on_main_window_close)

    login_window = LoginWindow(root, on_user_selected)

    root.mainloop()

if __name__ == "__main__":
    main()