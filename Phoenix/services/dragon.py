from sqlalchemy.orm import Session
from models import Dragon, Task, MicroHabit
from schemas.dragon import DragonCreate, DragonUpdate
from typing import List
from datetime import datetime


class DragonService:
    @staticmethod
    def create_dragon(db: Session, dragon: DragonCreate, user_id: int):
        db_dragon = Dragon(**dragon.model_dump(), user_id=user_id)
        db.add(db_dragon)
        db.commit()
        db.refresh(db_dragon)
        return db_dragon

    @staticmethod
    def get_dragon(db: Session, dragon_id: int):
        return db.query(Dragon).filter(Dragon.id == dragon_id).first()

    @staticmethod
    def get_user_dragons(db: Session, user_id: int):
        return db.query(Dragon).filter(Dragon.user_id == user_id).all()

    @staticmethod
    def update_dragon(db: Session, dragon_id: int, dragon: DragonUpdate):
        db_dragon = db.query(Dragon).filter(Dragon.id == dragon_id).first()
        if db_dragon:
            for key, value in dragon.model_dump(exclude_unset=True).items():
                setattr(db_dragon, key, value)
            db.commit()
            db.refresh(db_dragon)
        return db_dragon

    @staticmethod
    def delete_dragon(db: Session, dragon_id: int):
        db_dragon = db.query(Dragon).filter(Dragon.id == dragon_id).first()
        if db_dragon:
            db.delete(db_dragon)
            db.commit()
        return db_dragon

    @staticmethod
    def update_dragon_progress(db: Session, dragon_id: int, progress: int) -> Dragon:
        db_dragon = db.query(Dragon).filter(Dragon.id == dragon_id).first()
        if db_dragon:
            db_dragon.progress = max(0, progress)

            if db_dragon.progress >= db_dragon.progress_threshold:
                db_dragon.status = "slayed"
                db_dragon.end_date = datetime.now()
                db_dragon.progress = db_dragon.progress_threshold

            db.commit()
            db.refresh(db_dragon)
        return db_dragon

    @staticmethod
    def get_active_dragons(db: Session, user_id: int) -> List[Dragon]:
        return (
            db.query(Dragon)
            .filter(Dragon.user_id == user_id, Dragon.status == "active")
            .all()
        )

    @staticmethod
    def get_slayed_dragons(db: Session, user_id: int) -> List[Dragon]:
        return (
            db.query(Dragon)
            .filter(Dragon.user_id == user_id, Dragon.status == "slayed")
            .all()
        )

    @staticmethod
    def get_dragons_by_difficulty(
        db: Session, user_id: int, difficulty: int
    ) -> List[Dragon]:
        return (
            db.query(Dragon)
            .filter(Dragon.user_id == user_id, Dragon.difficulty == difficulty)
            .all()
        )

    @staticmethod
    def get_dragon_tasks(db: Session, dragon_id: int) -> List[Task]:
        dragon = db.query(Dragon).filter(Dragon.id == dragon_id).first()
        return dragon.tasks if dragon else []

    @staticmethod
    def get_dragon_micro_habits(db: Session, dragon_id: int) -> List[MicroHabit]:
        dragon = db.query(Dragon).filter(Dragon.id == dragon_id).first()
        return dragon.micro_habits if dragon else []

    @staticmethod
    def add_task_to_dragon(db: Session, dragon_id: int, task_id: int) -> Dragon:
        dragon = db.query(Dragon).filter(Dragon.id == dragon_id).first()
        task = db.query(Task).filter(Task.id == task_id).first()
        if dragon and task:
            dragon.tasks.append(task)
            db.commit()
            db.refresh(dragon)
        return dragon

    @staticmethod
    def add_micro_habit_to_dragon(
        db: Session, dragon_id: int, micro_habit_id: int
    ) -> Dragon:
        dragon = db.query(Dragon).filter(Dragon.id == dragon_id).first()
        micro_habit = (
            db.query(MicroHabit).filter(MicroHabit.id == micro_habit_id).first()
        )
        if dragon and micro_habit:
            dragon.micro_habits.append(micro_habit)
            db.commit()
            db.refresh(dragon)
        return dragon

    @staticmethod
    def get_dragon_stats(db: Session, dragon_id: int):
        dragon = db.query(Dragon).filter(Dragon.id == dragon_id).first()
        if dragon:
            return {
                "name": dragon.name,
                "description": dragon.description,
                "status": dragon.status,
                "progress": dragon.progress,
                "difficulty": dragon.difficulty,
                "start_date": dragon.start_date,
                "end_date": dragon.end_date,
                "xp_reward": dragon.xp_reward,
                "tasks_count": len(dragon.tasks),
                "micro_habits_count": len(dragon.micro_habits),
            }
        return None
