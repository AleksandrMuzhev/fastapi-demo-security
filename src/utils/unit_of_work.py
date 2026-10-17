# src/utils/unit_of_work.py
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.user_repo import UserRepository


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.users = UserRepository(session)
        # Здесь можно добавить другие репозитории
        # self.tasks = TaskRepository(session)
        # self.payments = PaymentRepository(session)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()