from fastapi import Depends, HTTPException, status

from app.admins.dao import AdminsDao
from app.users.dependencies import get_current_user


async def get_current_admin(current_user: dict = Depends(get_current_user)):
    user = await AdminsDao.find_one_or_none(user_id=int(current_user.id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    return user

