import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Get the current directory (where database.py is located)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the database file in the models folder
db_path = os.path.join(current_dir, 'phoenix.db')

# Create the SQLAlchemy database URI
SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'

engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()