from pydantic import BaseModel, ConfigDict
from datetime import datetime
from .mission import MissionStatus

class MissionBase(BaseModel):
    name: str
    description: str
    difficulty: int
    start_date: datetime
    end_date: datetime

class MissionCreate(MissionBase):
    pass

class Mission(MissionBase):
    id: int
    status: MissionStatus
    progress: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)