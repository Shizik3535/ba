from fastapi import HTTPException, status
import shutil
from PIL import Image as PILImage
import os

from app.config import settings
from app.users.dao import UsersDao
from app.users.auth import verify_password, get_password_hash
from app.users.profile.shemas import SProfile


async def c_get_profile(current_user: dict):
    return await UsersDao.info(current_user.id)


async def c_get_profile_by_id(user_id: int, current_user: dict):
    if current_user:
        result = await UsersDao.info(user_id)
        if result == {}:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
        else:
            return result
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")


async def c_change_username(data: dict, current_user: dict):
    if current_user:
        if not verify_password(data.password, current_user.hashed_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный пароль")
        else:
            await UsersDao.update(current_user.id, username=data.username)
            return {"message": "Логин пользователя успешно изменено"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")


async def c_change_password(data: dict, current_user: dict):
    if current_user:
        if not verify_password(data.old_password, current_user.hashed_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный пароль")
        else:
            hashed_password = get_password_hash(data.new_password)
            if data.new_password == data.old_password:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Новый пароль совпадает с старым")
            else:
                await UsersDao.update(current_user.id, hashed_password=hashed_password)
                return {"message": "Пароль пользователя успешно изменен"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")


async def c_change_email(data: dict, current_user: dict):
    if current_user:
        if not verify_password(data.password, current_user.hashed_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный пароль")
        if data.email == current_user.email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Новый email совпадает с старым")
        await UsersDao.update(current_user.id, email=data.email)
        return {"message": "Email пользователя успешно изменен"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

async def c_change_avatar(image, current_user: dict):
    if current_user:
        image_types = ["image/png", "image/jpeg", "image/jpg", "image/webp", "image/svg", "image/bmp"]
        if image.content_type not in image_types:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный тип изображения")
        if image.size > 5 * 1024 * 1024:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Слишком большое изображение")
        with open(f"app/media/avatars/{current_user.id}.webp", "wb") as file_obj:
            shutil.copyfileobj(image.file, file_obj)

        img = PILImage.open(f"app/media/avatars/{current_user.id}.webp")
        img.save(f"app/media/avatars/{current_user.id}.webp", "webp", quality=80, method=6)
        await UsersDao.update(int(current_user.id), avatar=f"http://{settings.DOMAIN}/media/avatars/{current_user.id}.webp")
        return {"message": "Аватар обновлен"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")



async def c_delete_avatar(current_user: SProfile):
    if current_user.avatar == f"http://{settings.DOMAIN}/media/avatars/default_male.webp" or current_user.avatar == f"http://{settings.DOMAIN}/media/avatars/default_female.webp":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Аватар по умолчанию не может быть удален",
        )

    await UsersDao.delete_avatar(int(current_user.id), current_user.gender)

    if os.path.isfile(f"app/media/avatars/{current_user.id}.webp"):
        os.remove(f"app/media/avatars/{current_user.id}.webp")
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Аватар не найден",
        )

    return {"message": "Аватар удален"}