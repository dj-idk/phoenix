from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class Progress(Base):
    __tablename__ = 'progress'

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float)
    unit = Column(String)
    date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    mission_id = Column(Integer, ForeignKey('missions.id'))
    mission = relationship("Mission", back_populates="progress_entries")
    dragon_id = Column(Integer, ForeignKey('dragons.id'))
    dragon = relationship("Dragon", back_populates="progress_entries")