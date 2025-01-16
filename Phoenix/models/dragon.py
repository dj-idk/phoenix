from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base
from enum import Enum as PyEnum 

class DragonStatus(PyEnum):
    ACTIVE = 'active'
    SLAYED = 'slayed'

dragon_life_areas = Table('dragon_life_areas', Base.metadata,
                          Column('dragon_id',Integer, ForeignKey('dragons.id')),
                          Column('life_area_id', Integer, ForeignKey('life_areas.id')))

dragon_micro_habits = Table('dragon_micro_habits', Base.metadata,
                            Column('dragon_id', Integer, ForeignKey('dragons.id')),
                            Column('micro_habit_id', Integer, ForeignKey('micro_habits.id')))
dragon_tasks = Table('dragon_tasks', Base.metadata,
                     Column('dragon_id', Integer, ForeignKey('dragons.id')),
                     Column('task_id', Integer, ForeignKey('tasks.id')))


class Dragon(Base):
    __tablename__ = 'dragons'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    status = Column(Enum(DragonStatus), default=DragonStatus.ACTIVE)
    progress = Column(Integer, default=0)
    difficulty = Column(Integer)
    xp_reward = Column(Integer)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    life_areas = relationship('LifeArea', secondary=dragon_life_areas, back_populates='dragons')
    micro_habits = relationship('MicroHabit',secondary=dragon_micro_habits, back_populates='dragons')
    tasks = relationship("Task",secondary=dragon_tasks ,back_populates="dragons")
    progress_entries = relationship("Progress", back_populates="dragon")

    @property
    def xp_reward(self):
        if self.start_date and self.end_date:
            duration = (self.end_date - self.start_date).days
            return duration * self.difficulty
        return 0