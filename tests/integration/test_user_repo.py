# tests/integration/test_user_repo.py
import psycopg2
import pytest

from src.repositories.user_repo import UserRepository


@pytest.mark.asyncio
async def test_create_user(async_session):
    repo = UserRepository(async_session)

    user = await repo.create({
        "email": "test@example.com",
        "name": "Test User",
        "hashed_password": "hashed",
        "role": "USER"
    })

    assert user.id is not None
    assert user.email == "test@example.com"


@pytest.mark.asyncio
async def test_get_user_by_email(async_session):
    repo = UserRepository(async_session)

    await repo.create({
        "email": "find@example.com",
        "name": "Find Me",
        "hashed_password": "hashed",
        "role": "USER"
    })

    found = await repo.get_by_email("find@example.com")
    assert found is not None
    assert found.name == "Find Me"
