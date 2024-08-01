from fastapi import APIRouter, Depends

from app.admins.dependencies import get_current_admin
from app.admins.students.controllers import c_add_students
from app.admins.students.shemas import SAddStudents, SSuccessAddStudents


router = APIRouter(
    prefix="/admin/students",
    tags=["Администрирование_студенты"],
)


@router.post("")
async def add_students(data: SAddStudents, current_admin=Depends(get_current_admin)) -> :
    return await c_add_students(data)