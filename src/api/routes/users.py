# src/api/routes/users.py
from fastapi import APIRouter, Depends
from src.services.user_service import UserService
from src.api.dependencies import get_user_service
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/users", tags=["users"])


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    role: str

    class Config:
        from_attributes = True


"""
API (/{user_id}) -> Service -> Repository -> БД
"""

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
        user_id: int,
        service: UserService = Depends(get_user_service)
):
    return await service.get_user_profile(user_id)


@router.post("/", response_model=UserResponse)
async def create_user(
        data: UserCreate,
        service: UserService = Depends(get_user_service)
):
    return await service.register_user(data.email, data.name, data.password)