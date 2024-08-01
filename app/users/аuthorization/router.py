from fastapi import APIRouter, Response

from app.users.аuthorization.сontrollers import c_login, c_logout, c_register, c_checking_code
from app.users.аuthorization.shemas import SLogin, SRegistration, SSuccessLogin, SSuccess


router = APIRouter(
    prefix="/auth",
    tags=["Авторизация"],
)


@router.post("/login")
async def login(user_data: SLogin, response: Response) -> SSuccessLogin:
    return await c_login(user_data, response)


@router.post("/logout")
async def logout(response: Response) -> SSuccess:
    return await c_logout(response)


@router.get("/registration/{code}")
async def checking_code(code: str) -> bool:
    return await c_checking_code(code)


@router.post("/registration/{code}")
async def registration(code: str, user_data: SRegistration, response: Response) -> SSuccess:
    return await c_register(code, user_data, response)

