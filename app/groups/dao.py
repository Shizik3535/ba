from sqlalchemy import select, insert, delete, update

from app.database import async_session_maker
from app.dao.dao import BaseDao

from app.groups.model import Groups, StudentsGroups


class GroupsDao(BaseDao):
    model = Groups


class StudentsGroupsDao(BaseDao):
    model = StudentsGroups

