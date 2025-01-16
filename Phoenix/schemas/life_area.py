from pydantic import BaseModel, ConfigDict
from datetime import datetime

class LifeAreaBase(BaseModel):
    name: str
    category: str
    heaven_scenario: str
    hell_scenario: str

class LifeAreaCreate(LifeAreaBase):
    user_id: int

class LifeArea(LifeAreaBase):
    id: int
    level: int
    xp: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)