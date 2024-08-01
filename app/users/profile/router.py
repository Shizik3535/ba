from fastapi import APIRouter, Depends, Request, Response, UploadFile, File

from app.users.dependencies import get_current_user
from app.users.profile.controllers import c_get_profile, c_get_profile_by_id, c_change_username, c_change_password, c_change_avatar, c_delete_avatar, c_change_email
from app.users.profile.shemas import SProfile, SChangeUsername, SChangePassword, SChangeEmail, SSuccess


router = APIRouter(
    prefix="/profile",
    tags=["Пользователь"],
)


@router.get("")
async def get_profile(current_user=Depends(get_current_user)) -> SProfile:
    return await c_get_profile(current_user)


@router.get("/{user_id}")
async def get_profile_by_id(user_id: int, current_user=Depends(get_current_user)) -> SProfile:
    return await c_get_profile_by_id(user_id, current_user)


# @router.delete("")
# async def delete_profile():
#     pass


@router.put("/username")
async def change_username(data: SChangeUsername, current_user=Depends(get_current_user)) -> SSuccess:
    return await c_change_username(data, current_user)


@router.put("/password")
async def change_password(data: SChangePassword, current_user=Depends(get_current_user)) -> SSuccess:
    return await c_change_password(data, current_user)


@router.put("/email")
async def change_email(data: SChangeEmail, current_user=Depends(get_current_user)) -> SSuccess:
    return await c_change_email(data, current_user)


@router.put("/avatar")
async def change_avatar(image: UploadFile = File(...), current_user=Depends(get_current_user)) -> SSuccess:
    return await c_change_avatar(image, current_user)


@router.delete("/avatar")
async def delete_avatar(current_user=Depends(get_current_user)) -> SSuccess:
    return await c_delete_avatar(current_user)

