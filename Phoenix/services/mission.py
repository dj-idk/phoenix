from sqlalchemy.orm import Session
from models import Mission
from schemas.mission import MissionCreate, MissionUpdate


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
