# Базовый образ
FROM python:3.11-slim

# Установка зависимостей
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . .

# Создаем пользователя
RUN useradd -m -u 1000 appuser
USER appuser

# Запуск
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]