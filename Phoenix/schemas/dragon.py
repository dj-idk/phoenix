from pydantic import BaseModel, ConfigDict
from datetime import datetime
from models.dragon import DragonStatus

class DragonBase(BaseModel):
    name: str
    description: str
    difficulty: int
    xp_reward: int

class DragonCreate(DragonBase):
    pass

class Dragon(DragonBase):
    id:int
    life_area_id: int
    status: DragonStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)