from pydantic import BaseModel


class SLogin(BaseModel):
    username: str
    password: str


class SRegistration(BaseModel):
    code: str
    username: str
    password: str


class SSuccessLogin(BaseModel):
    access_token: str


class SSuccess(BaseModel):
    message: str