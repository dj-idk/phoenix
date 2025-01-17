from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum


class MissionStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    EXPIRED = "expired"


class MissionBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: MissionStatus = MissionStatus.ACTIVE
    progress: int = 0
    progress_threshold: int = 100
    difficulty: int
    awarded_xp: int = 0
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    user_declared_complete: bool = False


class MissionCreate(MissionBase):
    user_id: int


class MissionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[MissionStatus] = None
    progress: Optional[int] = None
    progress_threshold: Optional[int] = None
    difficulty: Optional[int] = None
    awarded_xp: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    user_declared_complete: Optional[bool] = None


class Mission(MissionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MissionInDB(Mission):
    pass
