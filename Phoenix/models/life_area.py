from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .mission import mission_life_areas
from .dragon import dragon_life_areas
from .micro_habit import life_area_micro_habits
from .base import Base


class LifeArea(Base):
    __tablename__ = "life_areas"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True)
    category = Column(String, index=True)
    level = Column(Integer, default=1)
    total_xp = Column(Integer, default=0)
    heaven_scenario = Column(String)
    hell_scenario = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # Relationships
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="life_areas")
    missions = relationship(
        "Mission", secondary=mission_life_areas, back_populates="life_areas"
    )
    dragons = relationship(
        "Dragon", secondary=dragon_life_areas, back_populates="life_areas"
    )
    microhabits = relationship(
        "MicroHabit", secondary=life_area_micro_habits, back_populates="life_areas"
    )
