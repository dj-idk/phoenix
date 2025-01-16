# Phoenix

Phoenix is a personal development and life management application designed to help users track their goals, habits, and overall life progress. It uses a GUI built with Tkinter and SQLAlchemy for database management.

## Features

- User Authentication
- User Profile Management
- Dashboard for Progress Overview
- Life Areas Tracking
- Mission Management
- Habit Tracking
- Dragon Metaphor for Challenges

## Project Structure
Phoenix/
├── gui/
│   ├── login_window.py
│   ├── main_window.py
│   ├── profile_editor.py
│   └── styles.py
├── models/
│   ├── base.py
│   ├── database.py
│   ├── dragon.py
│   ├── life_area.py
│   ├── micro_habit.py
│   ├── mission.py
│   ├── progress.py
│   ├── task.py
│   └── user.py
├── schemas/
│   ├── dragon.py
│   ├── life_area.py
│   ├── micro_habit.py
│   ├── mission.py
│   ├── progress.py
│   ├── task.py
│   └── user.py
├── services/
│   ├── dragon.py
│   ├── life_area.py
│   ├── micro_habit.py
│   ├── mission.py
│   ├── progress.py
│   ├── task.py
│   └── user.py
├── utils/
│   └── config.py
├── main.py
└── requirements.txt

## Installation

1. Clone the repository:
   git clone https://github.com/dj-idk/phoenix.git
   cd phoenix

2. Create a virtual environment and activate it:
   python -m venv env
   source env/bin/activate  # On Windows use env\Scripts\activate

3. Install the required packages:
   pip install -r requirements.txt

4. Run the application:
   python main.py

## Usage

After running the application, you'll be presented with a login window. Once logged in, you can:

- View and edit your profile
- Check your progress on the dashboard
- Manage your life areas
- Create and track missions
- Set up and monitor habits

## Development

This project uses:
- Tkinter for the GUI
- SQLAlchemy for ORM
- Alembic for database migrations

To make changes to the database schema:
1. Modify the relevant model in the `models/` directory
2. Create a new migration:
   alembic revision --autogenerate -m "Description of changes"
3. Apply the migration:
   alembic upgrade head

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
