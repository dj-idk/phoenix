from sqlalchemy.orm import Session
from ..models.progress import Progress
from ..schemas.progress import ProgressCreate, ProgressUpdate
from typing import List, Optional
from sqlalchemy import func
from datetime import datetime, timedelta


class ProgressService:
    @staticmethod
    def create_progress(
        db: Session, progress: ProgressCreate, user_id: int
    ) -> Progress:
        db_progress = Progress(
            user_id=user_id,
            value=progress.value,
            unit=progress.unit,
            xp_per_unit=progress.xp_per_unit,
            date=progress.date,
            mission_id=progress.mission_id,
            dragon_id=progress.dragon_id,
            micro_habit_id=progress.micro_habit_id,
        )
        db.add(db_progress)
        db.commit()
        db.refresh(db_progress)
        return db_progress

    @staticmethod
    def get_user_progress(db: Session, user_id: int) -> List[Progress]:
        return db.query(Progress).filter(Progress.user_id == user_id).all()

    @staticmethod
    def get_progress_by_entity(
        db: Session, user_id: int, entity_type: str, entity_id: int
    ) -> List[Progress]:
        return (
            db.query(Progress)
            .filter(
                Progress.user_id == user_id,
                getattr(Progress, f"{entity_type}_id") == entity_id,
            )
            .all()
        )

    @staticmethod
    def update_progress(
        db: Session, progress_id: int, progress: ProgressUpdate
    ) -> Optional[Progress]:
        db_progress = db.query(Progress).filter(Progress.id == progress_id).first()
        if db_progress:
            update_data = progress.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_progress, key, value)
            db.commit()
            db.refresh(db_progress)
        return db_progress

    @staticmethod
    def delete_progress(db: Session, progress_id: int) -> Optional[Progress]:
        db_progress = db.query(Progress).filter(Progress.id == progress_id).first()
        if db_progress:
            db.delete(db_progress)
            db.commit()
        return db_progress

    @staticmethod
    def get_total_xp(progress_entries: List[Progress]) -> float:
        return sum(entry.total_xp for entry in progress_entries)

    @staticmethod
    def get_progress_summary(
        db: Session,
        user_id: int,
        entity_type: Optional[str] = None,
        entity_id: Optional[int] = None,
    ) -> dict:
        query = db.query(Progress).filter(Progress.user_id == user_id)

        if entity_type and entity_id:
            query = query.filter(getattr(Progress, f"{entity_type}_id") == entity_id)

        progress_entries = query.all()

        return {
            "total_entries": len(progress_entries),
            "total_xp": ProgressService.get_total_xp(progress_entries),
            "units": set(entry.unit for entry in progress_entries),
            "latest_entry": (
                max(progress_entries, key=lambda x: x.date)
                if progress_entries
                else None
            ),
        }

    @staticmethod
    def get_progress_by_date_range(
        db: Session, user_id: int, start_date: datetime, end_date: datetime
    ) -> List[Progress]:
        return (
            db.query(Progress)
            .filter(
                Progress.user_id == user_id,
                Progress.date >= start_date,
                Progress.date <= end_date,
            )
            .all()
        )

    @staticmethod
    def get_progress_streak(
        db: Session, user_id: int, entity_type: str, entity_id: int
    ) -> int:
        progress_entries = (
            db.query(Progress)
            .filter(
                Progress.user_id == user_id,
                getattr(Progress, f"{entity_type}_id") == entity_id,
            )
            .order_by(Progress.date.desc())
            .all()
        )

        streak = 0
        last_date = datetime.now().date()

        for entry in progress_entries:
            if (last_date - entry.date.date()).days == 1:
                streak += 1
                last_date = entry.date.date()
            elif (last_date - entry.date.date()).days > 1:
                break
            else:
                last_date = entry.date.date()

        return streak

    @staticmethod
    def get_average_progress(
        db: Session, user_id: int, entity_type: str, entity_id: int, days: int
    ) -> float:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        average = (
            db.query(func.avg(Progress.value))
            .filter(
                Progress.user_id == user_id,
                getattr(Progress, f"{entity_type}_id") == entity_id,
                Progress.date >= start_date,
                Progress.date <= end_date,
            )
            .scalar()
        )

        return average or 0.0

    @staticmethod
    def get_progress_history(
        db: Session, user_id: int, entity_type: str, entity_id: int, limit: int = 10
    ) -> List[Progress]:
        return (
            db.query(Progress)
            .filter(
                Progress.user_id == user_id,
                getattr(Progress, f"{entity_type}_id") == entity_id,
            )
            .order_by(Progress.date.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_total_xp_by_entity(
        db: Session, user_id: int, entity_type: str, entity_id: int
    ) -> float:
        total_xp = (
            db.query(func.sum(Progress.value * Progress.xp_per_unit))
            .filter(
                Progress.user_id == user_id,
                getattr(Progress, f"{entity_type}_id") == entity_id,
            )
            .scalar()
        )
        return total_xp or 0.0
