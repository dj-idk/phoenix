from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Enum,
    Table,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base
from enum import Enum as PyEnum
from datetime import datetime


class MissionStatus(PyEnum):
    ACTIVE = "active"
    COMPLETED = "completed"
    EXPIRED = "expired"


mission_life_areas = Table(
    "mission_life_areas",
    Base.metadata,
    Column("mission_id", Integer, ForeignKey("missions.id")),
    Column("life_area_id", Integer, ForeignKey("life_areas.id")),
)

mission_tasks = Table(
    "mission_tasks",
    Base.metadata,
    Column("mission_id", Integer, ForeignKey("missions.id")),
    Column("task_id", Integer, ForeignKey("tasks.id")),
)

mission_micro_habits = Table(
    "mission_micro_habits",
    Base.metadata,
    Column("mission_id", Integer, ForeignKey("missions.id")),
    Column("micro_habit_id", Integer, ForeignKey("micro_habits.id")),
)


class Mission(Base):
    __tablename__ = "missions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    status = Column(Enum(MissionStatus), default=MissionStatus.ACTIVE)
    progress = Column(Integer, default=0)
    progress_threshold = Column(Integer, default=100)
    difficulty = Column(Integer)
    awarded_xp = Column(Integer, default=0)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    user_declared_complete = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="missions")
    life_areas = relationship(
        "LifeArea", secondary=mission_life_areas, back_populates="missions"
    )
    tasks = relationship("Task", secondary=mission_tasks, back_populates="missions")
    micro_habits = relationship(
        "MicroHabit", secondary=mission_micro_habits, back_populates="missions"
    )
    progress_entries = relationship("Progress", back_populates="mission")

    @property
    def potential_xp_reward(self):
        if self.start_date and self.end_date:
            planned_duration = (self.end_date - self.start_date).days
            if self.is_completed:
                actual_duration = (
                    datetime.now(self.end_date.tzinfo) - self.start_date
                ).days
                time_factor = max(
                    0.5, min(2, planned_duration / max(actual_duration, 1))
                )
            else:
                time_factor = 1
            return int(planned_duration * self.difficulty * time_factor)
        return 0

    @property
    def total_progress(self):
        return sum(entry.value for entry in self.progress_entries)

    @property
    def all_tasks_completed(self):
        return all(task.is_completed for task in self.tasks)

    @property
    def is_completed(self):
        return (
            self.total_progress >= self.progress_threshold
            or self.all_tasks_completed
            or self.user_declared_complete
            or (self.end_date and self.end_date < func.now())
        )

    def update_status(self):
        old_status = self.status
        if self.is_slayed:
            self.status = MissionStatus.COMPLETED
        elif self.end_date and self.end_date < func.now():
            self.status = MissionStatus.EXPIRED
        else:
            self.status = MissionStatus.ACTIVE

        if (
            self.status == MissionStatus.COMPLETED
            and old_status != MissionStatus.COMPLETED
        ):
            self.awarded_xp = self.potential_xp_reward

    def award_xp_to_user(self, user):
        if self.status == MissionStatus.COMPLETED and self.awarded_xp == 0:
            xp_to_award = self.potential_xp_reward
            user.overall_xp += xp_to_award
            self.awarded_xp = xp_to_award
