from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProgressBase(BaseModel):
    value: float
    unit: str
    date: datetime = datetime.now()

class ProgressCreate(ProgressBase):
    mission_id: Optional[int] = None
    dragon_id: Optional[int] = None

class Progress(ProgressBase):
    id: int
    mission_id: Optional[int]
    dragon_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True