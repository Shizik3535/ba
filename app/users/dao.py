from sqlalchemy import insert, select, update

from app.database import async_session_maker
from app.config import settings

from app.dao.dao import BaseDao

from app.users.model import Users, Registrations


class UsersDao(BaseDao):
    model = Users

    @classmethod
    async def create_user(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model.id)
            result = await session.execute(query)
            await session.commit()
            return result.scalar()


    @classmethod
    async def info(cls, user_id: int):
        async with async_session_maker() as session:
            query = select(
                cls.model.id,
                cls.model.first_name,
                cls.model.last_name,
                cls.model.middle_name,
                cls.model.gender,
                cls.model.avatar
            ).where(cls.model.id == user_id)
            result = await session.execute(query)
            data = {}
            for row in result:
                data.update(row._asdict())
            return data

    @classmethod
    async def delete_avatar(cls, user_id: int, gender: str):
        async with async_session_maker() as session:
            if gender == "Мужской":
                query = update(cls.model).where(cls.model.id == user_id).values(avatar=f"http://{settings.DOMAIN}/media/avatars/default_male.webp")
            elif gender == "Женский":
                query = update(cls.model).where(cls.model.id == user_id).values(avatar=f"http://{settings.DOMAIN}/media/avatars/default_female.webp")
            await session.execute(query)
            await session.commit()

class RegistrationsDao(BaseDao):
    model = Registrations

