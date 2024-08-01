from app.dao.dao import BaseDao
from app.admins.model import Admins


class AdminsDao(BaseDao):
    model = Admins

