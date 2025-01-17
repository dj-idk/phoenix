from sqlalchemy.orm import Session
from models import LifeArea
from schemas.life_area import LifeAreaCreate, LifeAreaUpdate
from typing import List


class LifeAreaService:
    @staticmethod
    def create_life_area(db: Session, life_area: LifeAreaCreate, user_id: int):
        db_life_area = LifeArea(**life_area.model_dump(), user_id=user_id)
        db.add(db_life_area)
        db.commit()
        db.refresh(db_life_area)
        return db_life_area

    @staticmethod
    def get_life_area_by_name_and_category(
        db: Session, name: str, category: str, user_id: int
    ):
        return (
            db.query(LifeArea)
            .filter(
                LifeArea.name == name,
                LifeArea.category == category,
                LifeArea.user_id == user_id,
            )
            .first()
        )

    @staticmethod
    def get_life_areas_by_user_id(db: Session, user_id: int):
        return db.query(LifeArea).filter(LifeArea.user_id == user_id).all()

    @staticmethod
    def update_life_area(db: Session, life_area_id: int, life_area: LifeAreaUpdate):
        db_life_area = db.query(LifeArea).filter(LifeArea.id == life_area_id).first()
        if db_life_area:
            for key, value in life_area.dict(exclude_unset=True).items():
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

    @staticmethod
    def update_life_area_xp(db: Session, life_area_id: int, xp_gained: int) -> LifeArea:
        db_life_area = db.query(LifeArea).filter(LifeArea.id == life_area_id).first()
        if db_life_area:
            db_life_area.xp += xp_gained
            db_life_area.level = LifeAreaService.calculate_level(db_life_area.xp)
            db.commit()
            db.refresh(db_life_area)
        return db_life_area

    @staticmethod
    def calculate_level(xp: int) -> int:
        level = 1
        xp_threshold = 100
        total_xp = 0

        while total_xp + xp_threshold <= xp:
            total_xp += xp_threshold
            level += 1
            xp_threshold += 10

        return level

    @staticmethod
    def get_top_life_areas(db: Session, user_id: int, limit: int = 5) -> List[LifeArea]:
        return (
            db.query(LifeArea)
            .filter(LifeArea.user_id == user_id)
            .order_by(LifeArea.level.desc(), LifeArea.xp.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_life_area_stats(db: Session, life_area_id: int):
        db_life_area = db.query(LifeArea).filter(LifeArea.id == life_area_id).first()
        if db_life_area:
            return {
                "name": db_life_area.name,
                "category": db_life_area.category,
                "level": db_life_area.level,
                "xp": db_life_area.xp,
                "description": db_life_area.description,
            }
        return None

    @staticmethod
    def reset_life_area_progress(db: Session, life_area_id: int) -> LifeArea:
        db_life_area = db.query(LifeArea).filter(LifeArea.id == life_area_id).first()
        if db_life_area:
            db_life_area.xp = 0
            db_life_area.level = 1
            db.commit()
            db.refresh(db_life_area)
        return db_life_area
