from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .mission import mission_micro_habits
from .dragon import dragon_micro_habits
from .base import Base
from enum import Enum as PyEnum


class FrequencyUnit(PyEnum):
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"


life_area_micro_habits = Table(
    "life_area_micro_habits",
    Base.metadata,
    Column("life_area_id", Integer, ForeignKey("life_areas.id")),
    Column("micro_habit_id", Integer, ForeignKey("micro_habits.id")),
)


class MicroHabit(Base):
    __tablename__ = "micro_habits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    frequency = Column(Integer)
    frequency_unit = Column(Enum(FrequencyUnit))
    streak_count = Column(Integer, default=0)
    xp_reward = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # Relationships
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="micro_habits")
    dragons = relationship(
        "Dragon", secondary=dragon_micro_habits, back_populates="micro_habits"
    )
    missions = relationship(
        "Mission", secondary=mission_micro_habits, back_populates="micro_habits"
    )
    life_areas = relationship(
        "LifeArea", secondary=life_area_micro_habits, back_populates="micro_habits"
    )
    progress_entries = relationship("Progress", back_populates="micro_habit")

    @property
    def completion_count(self):
        return sum(entry.value for entry in self.progress_entries)
