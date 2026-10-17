# src/services/user_service.py
from fastapi import HTTPException
from src.utils.unit_of_work import UnitOfWork

class UserService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_user_profile(self, user_id: int):
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(404, "User not found")
        return user

    async def register_user(self, email: str, name: str, password: str):
        async with self.uow as uow:
            # Проверка на дубликат
            existing = await uow.users.get_by_email(email)
            if existing:
                raise HTTPException(400, "Email already exists")

            hashed = f"hashed_{password}"

            user = await uow.users.create({
                "email": email,
                "name": name,
                "hashed_password": hashed,
                "role": "USER"
            })

            # Если всё успешно — автоматический commit
            return user