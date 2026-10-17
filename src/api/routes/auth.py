# src/api/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.api.schemas.auth import UserCreate, UserResponse, Token
from src.core.security import hash_password, verify_password, create_access_token, decode_token
from src.repositories.user_repo import UserRepository
from src.api.dependencies import get_user_repo
from src.api.dependencies import get_current_user
from src.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
async def register(
        user_data: UserCreate,
        repo: UserRepository = Depends(get_user_repo)
):
    # Проверка на существующего пользователя
    existing = await repo.get_by_email(user_data.email)
    if existing:
        raise HTTPException(400, "Email already registered")

    # Хеширование пароля
    hashed_password = hash_password(user_data.password)

    # Создание пользователя
    user = await repo.create({
        "email": user_data.email,
        "hashed_password": hashed_password,
        "name": user_data.name,
        "role": "USER"
    })

    return user


@router.post("/login", response_model=Token)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        repo: UserRepository = Depends(get_user_repo)
):
    # Поиск пользователя
    user = await repo.get_by_email(form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Проверка пароля
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Создание токена
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role}
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    return current_user





















