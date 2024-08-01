from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database import Base
from app.config import settings


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=True)
    hashed_password = Column(String, nullable=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    gender = Column(String, nullable=False)
    avatar = Column(String, nullable=True, default=f"http://{settings.DOMAIN}/media/default_avatar.png")
    email = Column(String, unique=True, nullable=True, default=None)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    activated_at = Column(DateTime, nullable=True)


class Registrations(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    code = Column(String, nullable=True)
    used = Column(Boolean, default=False)
    created_by = Column(ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=func.now())



