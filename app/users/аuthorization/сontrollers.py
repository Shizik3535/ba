from fastapi import Response, HTTPException, status
from sqlalchemy.sql import func

from app.users.dao import UsersDao, RegistrationsDao
from app.users.auth import authenticate_user, create_access_token, get_password_hash

from app.users.аuthorization.shemas import SLogin, SRegistration


async def c_login(user_data: SLogin, response: Response):
    user = await authenticate_user(username=user_data.username, password=user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный логин или пароль")
    access_token = create_access_token(data={"sub": str(user.id)})
    response.set_cookie("litestudy", access_token, httponly=True)
    return {"access_token": access_token}


async def c_logout(response: Response):
    response.delete_cookie("litestudy")
    return {"message": "Вы вышли из аккаунта"}


async def c_checking_code(code: str):
    exist_code = await RegistrationsDao.find_one_or_none(code=code)
    if exist_code is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Код не существует")
    if exist_code.used:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Код уже был использован")
    return True


async def c_register(code: str, user_data: SRegistration, response: Response):
    exist_code = await RegistrationsDao.find_one_or_none(code=code)
    if exist_code is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Код не существует")
    if exist_code.used:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Код уже был использован")

    await UsersDao.update(
        exist_code.user_id,
        is_active=True,
        username=user_data.username,
        hashed_password=get_password_hash(user_data.password),
        activated_at=func.now()
    )

    await RegistrationsDao.update(exist_code.id, used=True)
    response.status_code = status.HTTP_201_CREATED
    return {"message": "Вы успешно зарегистрировались"}

