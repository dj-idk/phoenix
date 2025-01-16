from sqlalchemy import Column, Integer, String, DateTime, Text 
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func 
from .base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    life_mission = Column(Text)
    heaven_scenario = Column(Text)
    hell_scenario = Column(Text)
    values = Column(Text) 
    current_focus = Column(String(255))
    overall_level = Column(Integer, default=1)
    overall_xp = Column(Integer, default=10)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # Relationships
    life_areas = relationship('LifeArea', back_populates='user')

    