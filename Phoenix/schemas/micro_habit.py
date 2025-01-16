from pydantic import BaseModel, ConfigDict
from datetime import datetime

class MicroHabitBase(BaseModel):
    name: str
    frequency: int
    xp_reward: int

class MicroHabitCreate(MicroHabitBase):
    life_area_id: int

class MicroHabit(MicroHabitBase):
    id: int
    streak_count: int
    life_area_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)