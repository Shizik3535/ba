from pydantic import BaseModel, EmailStr
from typing import Optional
import enum


class Gender(str, enum.Enum):
    male = "Мужской"
    female = "Женский"


class SProfile(BaseModel):
    id: int
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    gender: Gender
    avatar: str

    class Config:
        from_attributes = True


class SChangeUsername(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True


class SChangePassword(BaseModel):
    old_password: str
    new_password: str

    class Config:
        from_attributes = True


class SChangeEmail(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class SSuccess(BaseModel):
    message: str


