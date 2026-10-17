# src/api/routes/admin.py
from fastapi import APIRouter, Depends
from src.api.dependencies import RoleChecker
from src.models.user import User
from src.repositories.user_repo import UserRepository
from src.api.dependencies import get_user_repo

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users")
async def get_all_users(
    user: User = Depends(RoleChecker(["ADMIN"])),
    repo: UserRepository = Depends(get_user_repo)
):
    # В реальном приложении здесь был бы метод get_all
    return {"message": "List of all users", "requested_by": user.email}

@router.get("/dashboard")
async def admin_dashboard(
    user: User = Depends(RoleChecker(["ADMIN", "MANAGER"]))
):
    return {"message": "Admin dashboard", "role": user.role}