# src/vulnerable/app.py
from fastapi import FastAPI
from sqlalchemy import text
from fastapi.responses import HTMLResponse
from html import escape

app = FastAPI(title="Vulnerable App")

# Имитация БД
USERS = [
    {"id": 1, "email": "admin@example.com", "name": "Admin", "password": "secret123"},
    {"id": 2, "email": "user1@example.com", "name": "User 1", "password": "pass1"},
    {"id": 3, "email": "user2@example.com", "name": "User 2", "password": "pass2"},
]


# УЯЗВИМЫЙ эндпоинт
@app.get("/vulnerable/users")
def get_user_vulnerable(user_id: str):
    # НЕ ДЕЛАЙТЕ ТАК!
    # Имитация SQL-запроса с конкатенацией строк
    query = f"SELECT * FROM users WHERE id = {user_id}"
    print(f"Executing: {query}")

    # Имитация выполнения: если в запросе есть OR 1=1, возвращаем всех
    if "OR 1=1" in user_id or "or 1=1" in user_id.lower():
        return {"query": query, "result": USERS, "warning": "ALL USERS RETURNED!"}

    try:
        uid = int(user_id)
        user = next((u for u in USERS if u["id"] == uid), None)
        return {"query": query, "result": user}
    except ValueError:
        return {"query": query, "result": None, "error": "Invalid ID"}


# Безопасный эндпоинт
@app.get("/safe/users")
def get_user_safe(user_id: int):
    # Безопасно: валидация типа + ORM
    user = next((u for u in USERS if u["id"] == user_id), None)
    if not user:
        return {"result": None, "error": "User not found"}
    return {"result": user}


# УЯЗВИМЫЙ эндпоинт (XSS)
@app.get("/vulnerable/search", response_class=HTMLResponse)
def search_vulnerable(query: str):
    # НЕ ДЕЛАЙТЕ ТАК!
    # Возвращаем HTML с пользовательским вводом
    return f"<h1>Результаты поиска: {query}</h1>"


# БЕЗОПАСНЫЙ эндпоинт (XSS защита)
@app.get("/safe/search", response_class=HTMLResponse)
def search_safe(query: str):
    # Безопасно: экранирование
    safe_query = escape(query)
    return f"<h1>Результаты поиска: {safe_query}</h1>"

















