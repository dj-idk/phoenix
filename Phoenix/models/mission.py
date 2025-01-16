from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Table, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base
from enum import Enum as PyEnum

class MissionStatus(PyEnum):
    ACTIVE = "active"
    COMPLETED = "completed"

mission_life_areas = Table('mission_life_areas', Base.metadata,
    Column('mission_id', Integer, ForeignKey('missions.id')),
    Column('life_area_id', Integer, ForeignKey('life_areas.id'))
)

mission_micro_habits = Table('mission_micro_habits', Base.metadata,
    Column('mission_id', Integer, ForeignKey('missions.id')),
    Column('micro_habit_id', Integer, ForeignKey('micro_habits.id'))
)

mission_tasks = Table('mission_tasks', Base.metadata,
    Column('mission_id', Integer, ForeignKey('missions.id')),
    Column('task_id', Integer, ForeignKey('tasks.id'))
)

class Mission(Base):
    __tablename__ = "missions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    status = Column(Enum(MissionStatus), default=MissionStatus.ACTIVE)
    progress = Column(Integer, default=0)
    difficulty = Column(Integer)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    life_areas = relationship("LifeArea", secondary=mission_life_areas, back_populates="missions")
    micro_habits = relationship("MicroHabit", secondary=mission_micro_habits, back_populates="missions")
    tasks = relationship("Task", secondary=mission_tasks, back_populates="missions")
    progress_entries = relationship("Progress", back_populates="mission")

    @property
    def xp_reward(self):
        if self.start_date and self.end_date:
            duration = (self.end_date - self.start_date).days
            return duration * self.difficulty
        return 0