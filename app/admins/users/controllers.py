from fastapi import HTTPException, status, Response
from uuid import uuid4

from app.users.dao import UsersDao, RegistrationsDao
from app.admins.dao import AdminsDao
from app.admins.users.shemas import SUsers
from app.config import settings


async def c_add_user(data: SUsers, user_data: dict, response: Response):
    if data.gender == "Мужской":
        avatar = f"http://{settings.DOMAIN}/media/avatars/default_male.webp"
    elif data.gender == "Женский":
        avatar = f"http://{settings.DOMAIN}/media/avatars/default_female.webp"
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неизвестный пол",
        )

    user_id = await UsersDao.create_user(
        first_name=data.first_name,
        last_name=data.last_name,
        middle_name=data.middle_name,
        gender=data.gender,
        avatar=avatar
    )

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось создать пользователя",
        )

    if UsersDao.find_by_id(user_id) is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось создать пользователя",
        )

    code = str(uuid4())
    await RegistrationsDao.insert(user_id=user_id, code=code, created_by=user_data.user_id)

    response.status_code = status.HTTP_201_CREATED

    return {
        "user_id": user_id,
        "first_name": data.first_name,
        "last_name": data.last_name,
        "middle_name": data.middle_name,
        "code": code
    }


async def c_add_first_admin(user_data: dict, response: Response):
    if user_data.gender == "Мужской":
        avatar = f"http://{settings.DOMAIN}/media/avatars/default_male.webp"
    elif user_data.gender == "Женский":
        avatar = f"http://{settings.DOMAIN}/media/avatars/default_female.webp"
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неизвестный пол",
        )

    user_id = await UsersDao.create_user(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        middle_name=user_data.middle_name,
        gender=user_data.gender,
        avatar=avatar
    )

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось создать пользователя",
        )

    if UsersDao.find_by_id(user_id) is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось создать пользователя",
        )

    await AdminsDao.insert(user_id=user_id)
    code = str(uuid4())
    await RegistrationsDao.insert(user_id=user_id, code=code, created_by=user_id)
    response.status_code = status.HTTP_201_CREATED

    return {
        "user_id": user_id,
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
        "middle_name": user_data.middle_name,
        "code": code
    }

