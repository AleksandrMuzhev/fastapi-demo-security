# src/main.py
from fastapi import FastAPI
from src.api.routes import auth, users, admin, tasks, cache

app = FastAPI(title="Corporate API")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(tasks.router)
app.include_router(cache.router)

@app.get("/")
def root():
    return {"message": "API is running"}
