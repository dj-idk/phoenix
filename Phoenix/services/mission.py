from sqlalchemy.orm import Session
from schemas.mission import MissionCreate, MissionUpdate
from models import Mission, Task, MicroHabit
from schemas.mission import MissionCreate, MissionUpdate
from typing import List
from datetime import datetime


class MissionService:
    @staticmethod
    def create_mission(db: Session, mission: MissionCreate, user_id: int):
        db_mission = Mission(**mission.model_dump(), user_id=user_id)
        db.add(db_mission)
        db.commit()
        db.refresh(db_mission)
        return db_mission

    @staticmethod
    def get_mission_by_id(db: Session, mission_id: int):
        return db.query(Mission).filter(Mission.id == mission_id).first()

    @staticmethod
    def get_active_missions(db: Session, user_id: int):
        return (
            db.query(Mission)
            .filter(Mission.user_id == user_id, Mission.status == "active")
            .all()
        )

    @staticmethod
    def update_mission(db: Session, mission_id: int, mission: MissionUpdate):
        db_mission = db.query(Mission).filter(Mission.id == mission_id).first()
        if db_mission:
            for key, value in mission.model_dump(exclude_unset=True).items():
                setattr(db_mission, key, value)
            db.commit()
            db.refresh(db_mission)
        return db_mission

    @staticmethod
    def delete_mission(db: Session, mission_id: int):
        db_mission = db.query(Mission).filter(Mission.id == mission_id).first()
        if db_mission:
            db.delete(db_mission)
            db.commit()
        return db_mission

    @staticmethod
    def update_mission_progress(db: Session, mission_id: int, progress: int) -> Mission:
        db_mission = db.query(Mission).filter(Mission.id == mission_id).first()
        if db_mission:
            db_mission.progress = max(0, progress)  # Ensure progress is not negative

            # Check if progress meets or exceeds the threshold
            if db_mission.progress >= db_mission.progress_threshold:
                db_mission.status = "completed"
                db_mission.end_date = datetime.now()
                db_mission.progress = (
                    db_mission.progress_threshold
                )  # Cap progress at threshold

            db.commit()
            db.refresh(db_mission)
        return db_mission

    @staticmethod
    def get_completed_missions(db: Session, user_id: int) -> List[Mission]:
        return (
            db.query(Mission)
            .filter(Mission.user_id == user_id, Mission.status == "completed")
            .all()
        )

    @staticmethod
    def get_mission_tasks(db: Session, mission_id: int) -> List[Task]:
        mission = db.query(Mission).filter(Mission.id == mission_id).first()
        return mission.tasks if mission else []

    @staticmethod
    def get_mission_micro_habits(db: Session, mission_id: int) -> List[MicroHabit]:
        mission = db.query(Mission).filter(Mission.id == mission_id).first()
        return mission.micro_habits if mission else []

    @staticmethod
    def add_task_to_mission(db: Session, mission_id: int, task_id: int) -> Mission:
        mission = db.query(Mission).filter(Mission.id == mission_id).first()
        task = db.query(Task).filter(Task.id == task_id).first()
        if mission and task:
            mission.tasks.append(task)
            db.commit()
            db.refresh(mission)
        return mission

    @staticmethod
    def add_micro_habit_to_mission(
        db: Session, mission_id: int, micro_habit_id: int
    ) -> Mission:
        mission = db.query(Mission).filter(Mission.id == mission_id).first()
        micro_habit = (
            db.query(MicroHabit).filter(MicroHabit.id == micro_habit_id).first()
        )
        if mission and micro_habit:
            mission.micro_habits.append(micro_habit)
            db.commit()
            db.refresh(mission)
        return mission

    @staticmethod
    def get_mission_stats(db: Session, mission_id: int):
        mission = db.query(Mission).filter(Mission.id == mission_id).first()
        if mission:
            return {
                "name": mission.name,
                "description": mission.description,
                "status": mission.status,
                "progress": mission.progress,
                "difficulty": mission.difficulty,
                "start_date": mission.start_date,
                "end_date": mission.end_date,
                "xp_reward": mission.xp_reward,
                "tasks_count": len(mission.tasks),
                "micro_habits_count": len(mission.micro_habits),
            }
        return None
