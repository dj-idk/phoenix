from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base


class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float)
    unit = Column(String)
    xp_per_unit = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    dragon_id = Column(Integer, ForeignKey("dragons.id"))
    dragon = relationship("Dragon", back_populates="progress_entries")
    mission_id = Column(Integer, ForeignKey("missions.id"))
    mission = relationship("Mission", back_populates="progress_entries")
    micro_habit_id = Column(Integer, ForeignKey("micro_habits.id"))
    micro_habit = relationship("MicroHabit", back_populates="progress_entries")
    task_id = Column(Integer, ForeignKey("tasks.id"))
    task = relationship("Task", back_populates="progress_entries")

    @property
    def total_xp(self):
        return round(self.value * self.xp_per_unit)
