from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr
    life_mission: Optional[str] = None
    heaven_scenario: Optional[str] = None
    hell_scenario: Optional[str] = None
    values: Optional[str] = None
    current_focus: Optional[str] = None
    overall_level: int = 1
    overall_xp: int = 10

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    life_mission: Optional[str] = None
    heaven_scenario: Optional[str] = None
    hell_scenario: Optional[str] = None
    values: Optional[str] = None
    current_focus: Optional[str] = None
    overall_level: Optional[int] = None
    overall_xp: Optional[int] = None

class UserInDB(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

