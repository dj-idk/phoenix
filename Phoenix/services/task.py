from sqlalchemy.orm import Session
from models import Task
from schemas.task import TaskCreate, TaskUpdate


class TaskService:
    @staticmethod
    def create_task(db: Session, task: TaskCreate, user_id: int):
        db_task = Task(**task.model_dump(), user_id=user_id)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def get_task(db: Session, task_id: int):
        return db.query(Task).filter(Task.id == task_id).first()

    @staticmethod
    def get_user_tasks(db: Session, user_id: int):
        return db.query(Task).filter(Task.user_id == user_id).all()

    @staticmethod
    def update_task(db: Session, task_id: int, task: TaskUpdate):
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if db_task:
            for key, value in task.model_dump(exclude_unset=True).items():
                setattr(db_task, key, value)
            db.commit()
            db.refresh(db_task)
        return db_task

    @staticmethod
    def delete_task(db: Session, task_id: int):
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if db_task:
            db.delete(db_task)
            db.commit()
        return db_task
