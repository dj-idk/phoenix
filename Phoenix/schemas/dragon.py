from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum


class DragonStatus(str, Enum):
    ACTIVE = "active"
    SLAYED = "slayed"
    ESCAPED = "escaped"


class DragonBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: DragonStatus = DragonStatus.ACTIVE
    progress: int = 0
    progress_threshold: int = 100
    difficulty: int
    awarded_xp: int = 0
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    user_declared_slayed: bool = False


class DragonCreate(DragonBase):
    user_id: int


class DragonUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[DragonStatus] = None
    progress: Optional[int] = None
    progress_threshold: Optional[int] = None
    difficulty: Optional[int] = None
    awarded_xp: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    user_declared_slayed: Optional[bool] = None


class Dragon(DragonBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    total_progress: int
    is_slayed: bool
    potential_xp_reward: int

    model_config = ConfigDict(from_attributes=True)


class DragonWithRelations(Dragon):
    life_areas: List[int] = []  # List of life area IDs
    tasks: List[int] = []  # List of task IDs
    micro_habits: List[int] = []  # List of micro habit IDs
    progress_entries: List[int] = []  # List of progress entry IDs
