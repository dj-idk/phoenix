from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class ProgressBase(BaseModel):
    value: float
    unit: str
    xp_per_unit: float


class ProgressCreate(ProgressBase):
    dragon_id: Optional[int] = None
    mission_id: Optional[int] = None
    micro_habit_id: Optional[int] = None
    task_id: Optional[int] = None


class ProgressUpdate(BaseModel):
    value: Optional[float] = None
    unit: Optional[str] = None
    xp_per_unit: Optional[float] = None
    dragon_id: Optional[int] = None
    mission_id: Optional[int] = None
    micro_habit_id: Optional[int] = None
    task_id: Optional[int] = None


class Progress(ProgressBase):
    id: int
    created_at: datetime
    updated_at: datetime
    total_xp: float
    dragon_id: Optional[int] = None
    mission_id: Optional[int] = None
    micro_habit_id: Optional[int] = None
    task_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class ProgressWithRelations(Progress):
    dragon: Optional[int] = None  # Dragon ID
    mission: Optional[int] = None  # Mission ID
    micro_habit: Optional[int] = None  # MicroHabit ID
    task: Optional[int] = None  # Task ID
