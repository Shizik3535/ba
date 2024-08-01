from fastapi import APIRouter, Depends, Response

from app.admins.dependencies import get_current_admin
from app.admins.users.controllers import c_add_user, c_add_first_admin
from app.admins.users.shemas import SUsers


router = APIRouter(
    prefix="/admin/users",
    tags=["Администрирование_пользователи"],
)


@router.post("/add_admin")
async def add_first_admin(data: SUsers, response: Response):
    return await c_add_first_admin(data, response)


@router.post("/add")
async def add_user(data: SUsers, response: Response, current_admin=Depends(get_current_admin)):
    return await c_add_user(data=data, user_data=current_admin, response=response)


@router.patch("/{id}/edit")
async def edit_user():
    pass


@router.delete("/{id}/delete")
async def delete_user():
    pass


