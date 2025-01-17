from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    ForeignKey,
    Table,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base
from enum import Enum as PyEnum
from datetime import datetime


class DragonStatus(PyEnum):
    ACTIVE = "active"
    SLAYED = "slayed"
    ESCAPED = "escaped"


dragon_life_areas = Table(
    "dragon_life_areas",
    Base.metadata,
    Column("dragon_id", Integer, ForeignKey("dragons.id")),
    Column("life_area_id", Integer, ForeignKey("life_areas.id")),
)

dragon_tasks = Table(
    "dragon_tasks",
    Base.metadata,
    Column("dragon_id", Integer, ForeignKey("dragons.id")),
    Column("task_id", Integer, ForeignKey("tasks.id")),
)

dragon_micro_habits = Table(
    "dragon_micro_habits",
    Base.metadata,
    Column("dragon_id", Integer, ForeignKey("dragons.id")),
    Column("micro_habit_id", Integer, ForeignKey("micro_habits.id")),
)


class Dragon(Base):
    __tablename__ = "dragons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    status = Column(Enum(DragonStatus), default=DragonStatus.ACTIVE)
    progress = Column(Integer, default=0)
    progress_threshold = Column(Integer, default=100)
    difficulty = Column(Integer)
    awarded_xp = Column(Integer, default=0)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    user_declared_slayed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="dragons")
    life_areas = relationship(
        "LifeArea", secondary=dragon_life_areas, back_populates="dragons"
    )
    tasks = relationship("Task", secondary=dragon_tasks, back_populates="dragons")
    micro_habits = relationship(
        "MicroHabit", secondary=dragon_micro_habits, back_populates="dragons"
    )
    progress_entries = relationship("Progress", back_populates="dragon")

    @property
    def potential_xp_reward(self):
        if self.start_date and self.end_date:
            planned_duration = (self.end_date - self.start_date).days
            if self.is_slayed:
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
    def is_slayed(self):
        return (
            self.total_progress >= self.progress_threshold
            or self.all_tasks_completed
            or self.user_declared_slayed
            or (self.end_date and self.end_date < func.now())
        )

    def update_status(self):
        old_status = self.status
        if self.is_slayed:
            self.status = DragonStatus.SLAYED
        elif self.end_date and self.end_date < func.now():
            self.status = DragonStatus.ESCAPED
        else:
            self.status = DragonStatus.ACTIVE

        if self.status == DragonStatus.SLAYED and old_status != DragonStatus.SLAYED:
            self.awarded_xp = self.potential_xp_reward

    def award_xp_to_user(self, user):
        if self.status == DragonStatus.SLAYED and self.awarded_xp == 0:
            xp_to_award = self.potential_xp_reward
            user.overall_xp += xp_to_award
            self.awarded_xp = xp_to_award
