from fastapi import HTTPException, status

from app.admins.dao import AdminsDao
from app.groups.dao import GroupsDao
from app.users.dao import UsersDao


async def c_add_students(data: dict, current_admin: dict):
    if current_admin:
