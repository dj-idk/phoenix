from sqlalchemy.orm import Session
from models import MicroHabit
from schemas.micro_habit import MicroHabitCreate, MicroHabitUpdate
from typing import List
from datetime import datetime, timedelta


class MicroHabitService:
    @staticmethod
    def create_micro_habit(db: Session, micro_habit: MicroHabitCreate, user_id: int):
        db_micro_habit = MicroHabit(**micro_habit.model_dump(), user_id=user_id)
        db.add(db_micro_habit)
        db.commit()
        db.refresh(db_micro_habit)
        return db_micro_habit

    @staticmethod
    def get_micro_habit(db: Session, micro_habit_id: int):
        return db.query(MicroHabit).filter(MicroHabit.id == micro_habit_id).first()

    @staticmethod
    def get_user_micro_habits(db: Session, user_id: int):
        return db.query(MicroHabit).filter(MicroHabit.user_id == user_id).all()

    @staticmethod
    def update_micro_habit(
        db: Session, micro_habit_id: int, micro_habit: MicroHabitUpdate
    ):
        db_micro_habit = (
            db.query(MicroHabit).filter(MicroHabit.id == micro_habit_id).first()
        )
        if db_micro_habit:
            for key, value in micro_habit.model_dump(exclude_unset=True).items():
                setattr(db_micro_habit, key, value)
            db.commit()
            db.refresh(db_micro_habit)
        return db_micro_habit

    @staticmethod
    def delete_micro_habit(db: Session, micro_habit_id: int):
        db_micro_habit = (
            db.query(MicroHabit).filter(MicroHabit.id == micro_habit_id).first()
        )
        if db_micro_habit:
            db.delete(db_micro_habit)
            db.commit()
        return db_micro_habit

    @staticmethod
    def get_top_streaks(db: Session, user_id: int, limit: int = 3):
        return (
            db.query(MicroHabit)
            .filter(MicroHabit.user_id == user_id)
            .order_by(MicroHabit.streak_count.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def increment_streak(db: Session, micro_habit_id: int):
        db_micro_habit = (
            db.query(MicroHabit).filter(MicroHabit.id == micro_habit_id).first()
        )
        if db_micro_habit:
            db_micro_habit.streak_count += 1
            db_micro_habit.last_completed = datetime.now()
            db.commit()
            db.refresh(db_micro_habit)
        return db_micro_habit

    @staticmethod
    def reset_streak(db: Session, micro_habit_id: int):
        db_micro_habit = (
            db.query(MicroHabit).filter(MicroHabit.id == micro_habit_id).first()
        )
        if db_micro_habit:
            db_micro_habit.streak_count = 0
            db.commit()
            db.refresh(db_micro_habit)
        return db_micro_habit

    @staticmethod
    def get_micro_habits_by_frequency(
        db: Session, user_id: int, frequency: int
    ) -> List[MicroHabit]:
        return (
            db.query(MicroHabit)
            .filter(MicroHabit.user_id == user_id, MicroHabit.frequency == frequency)
            .all()
        )

    @staticmethod
    def get_micro_habits_due_today(db: Session, user_id: int) -> List[MicroHabit]:
        today = datetime.now().date()
        return (
            db.query(MicroHabit)
            .filter(
                MicroHabit.user_id == user_id,
                (MicroHabit.last_completed == None)
                | (MicroHabit.last_completed < today),
            )
            .all()
        )
