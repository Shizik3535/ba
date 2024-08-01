from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.users.аuthorization.router import router as auth_router
from app.users.profile.router import router as profile_router
from app.admins.users.router import router as admin_users_router


app = FastAPI()


@app.get("/api/test")
async def root():
    return {"message": "Hello World"}


app.mount("/media", StaticFiles(directory="app/media"), name="media")


app.include_router(auth_router, prefix="/api")
app.include_router(profile_router, prefix="/api")
app.include_router(admin_users_router, prefix="/api")


