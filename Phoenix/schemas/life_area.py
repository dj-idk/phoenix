from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from .mission import MissionBase
from .dragon import DragonBase
from .micro_habit import MicroHabitBase


class LifeAreaBase(BaseModel):
    name: str
    category: Optional[str] = None
    level: int = 1
    total_xp: int = 0
    heaven_scenario: Optional[str] = None
    hell_scenario: Optional[str] = None


class LifeAreaCreate(LifeAreaBase):
    pass


class LifeAreaUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    level: Optional[int] = None
    total_xp: Optional[int] = None
    heaven_scenario: Optional[str] = None
    hell_scenario: Optional[str] = None


class LifeAreaInDB(LifeAreaBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    missions: List[MissionBase] = []
    dragons: List[DragonBase] = []
    microhabits: List[MicroHabitBase] = []

    model_config = ConfigDict(from_attributes=True)
