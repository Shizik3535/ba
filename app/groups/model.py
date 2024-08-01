from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database import Base


class Groups(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    tutor = Column(ForeignKey("users.id"), nullable=False)
    head = Column(ForeignKey("users.id"), nullable=True)
    deputy_head = Column(ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=func.now())


class StudentsGroups(Base):
    __tablename__ = "students_groups"

    id = Column(Integer, primary_key=True)
    group_id = Column(ForeignKey("groups.id"), nullable=False)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    created_by = Column(ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())