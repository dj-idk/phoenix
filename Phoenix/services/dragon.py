from sqlalchemy.orm import Session
from models import Dragon
from schemas.dragon import DragonCreate, DragonUpdate


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
