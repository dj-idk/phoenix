from sqlalchemy.orm import Session
from models import User
from schemas.user import UserCreate, UserUpdate
from typing import List

class UserService:
    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        db_user = User(name=user.name, email=user.email)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_user(db: Session, user_id: int) -> User:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def update_user(db: Session, user_id: int, user_update: UserUpdate):
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            update_data = user_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_user, key, value)
            db.commit()
            db.refresh(db_user)
        return db_user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> User:
        db_user = UserService.get_user(db, user_id)
        if db_user:
            db.delete(db_user)
            db.commit()
        return db_user