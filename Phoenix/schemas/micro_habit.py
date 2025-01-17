from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum


class FrequencyUnit(str, Enum):
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"


class MicroHabitBase(BaseModel):
    name: str
    frequency: int
    frequency_unit: FrequencyUnit
    xp_reward: int


class MicroHabitCreate(MicroHabitBase):
    user_id: int


class MicroHabitUpdate(BaseModel):
    name: Optional[str] = None
    frequency: Optional[int] = None
    frequency_unit: Optional[FrequencyUnit] = None
    xp_reward: Optional[int] = None
    streak_count: Optional[int] = None


class MicroHabit(MicroHabitBase):
    id: int
    user_id: int
    streak_count: int
    created_at: datetime
    updated_at: datetime
    completion_count: int

    model_config = ConfigDict(from_attributes=True)


class MicroHabitWithRelations(MicroHabit):
    dragons: List[int] = []  # List of dragon IDs
    missions: List[int] = []  # List of mission IDs
    life_areas: List[int] = []  # List of life area IDs
    progress_entries: List[int] = []  # List of progress entry IDs
