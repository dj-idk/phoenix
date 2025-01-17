from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime


class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None


class Task(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime
    completion_percentage: float
    is_completed: bool

    model_config = ConfigDict(from_attributes=True)


class TaskWithRelations(Task):
    missions: List[int] = []  # List of mission IDs
    dragons: List[int] = []  # List of dragon IDs
    progress_entries: List[int] = []  # List of progress entry IDs
