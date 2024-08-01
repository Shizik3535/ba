from pydantic import BaseModel
from typing import Optional
import enum


class Gender(str, enum.Enum):
    male = "Мужской"
    female = "Женский"


class SUsers(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    gender: Gender

