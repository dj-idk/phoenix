from sqlalchemy.orm import Session
from models import LifeArea
from schemas.life_area import LifeAreaCreate

class LifeAreaService:
    @staticmethod
    def create_life_area(db: Session, life_area: LifeAreaCreate):
        db_life_area = LifeArea(
            name=life_area.name,
            category=life_area.category,
            user_id=life_area.user_id,
            heaven_scenario=life_area.heaven_scenario,
            hell_scenario=life_area.hell_scenario
        )
        db.add(db_life_area)
        db.commit()
        db.refresh(db_life_area)
        return db_life_area

    @staticmethod
    def get_life_area_by_name_and_category(db: Session, name: str, category: str, user_id: int):
        return db.query(LifeArea).filter(
            LifeArea.name == name,
            LifeArea.category == category,
            LifeArea.user_id == user_id
        ).first()

    @staticmethod
    def get_life_areas_by_user_id(db: Session, user_id: int):
        return db.query(LifeArea).filter(LifeArea.user_id == user_id).all()

    @staticmethod
    def update_life_area(db: Session, life_area_id: int, life_area_data: dict):
        db_life_area = db.query(LifeArea).filter(LifeArea.id == life_area_id).first()
        if db_life_area:
            for key, value in life_area_data.items():
                setattr(db_life_area, key, value)
            db.commit()
            db.refresh(db_life_area)
        return db_life_area

    @staticmethod
    def delete_life_area(db: Session, life_area_id: int):
        db_life_area = db.query(LifeArea).filter(LifeArea.id == life_area_id).first()
        if db_life_area:
            db.delete(db_life_area)
            db.commit()
        return db_life_area