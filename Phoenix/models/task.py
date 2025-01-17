from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .mission import mission_tasks
from .dragon import dragon_tasks
from .base import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    is_completed = Column(Boolean, default=False)
    due_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    missions = relationship("Mission", secondary=mission_tasks, back_populates="tasks")
    dragons = relationship("Dragon", secondary=dragon_tasks, back_populates="tasks")
    progress_entries = relationship("Progress", back_populates="task")

    @property
    def completion_percentage(self):
        return sum(entry.value for entry in self.progress_entries)

    @property
    def is_completed(self):
        return self.completion_percentage >= 100
