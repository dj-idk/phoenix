from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .mission import mission_micro_habits
from .dragon import dragon_micro_habits
from .base import Base



class MicroHabit(Base):
    __tablename__ = 'micro_habits'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index = True)
    frequency = Column(Integer)
    streak_count = Column(Integer, default=0)
    xp_reward = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # Relationships
    missions = relationship('Mission', secondary=mission_micro_habits, back_populates='micro_habits')
    dragons = relationship('Dragon', secondary=dragon_micro_habits, back_populates='micro_habits')