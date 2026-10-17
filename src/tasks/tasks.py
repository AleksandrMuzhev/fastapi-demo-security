# src/tasks/tasks.py
from src.tasks.celery_app import app
from datetime import datetime

@app.task
def send_email(email: str, subject: str, body: str):
    """Отправка email в фоновом режиме"""
    # Имитация отправки
    print(f"Sending email to {email}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")
    return {"status": "sent", "email": email, "time": str(datetime.utcnow())}

@app.task(bind=True, max_retries=3)
def process_payment(self, user_id: int, amount: int):
    """Обработка платежа с повторными попытками"""
    try:
        # Имитация внешнего API
        print(f"Processing payment for user {user_id}, amount {amount}")
        return {"status": "success", "user_id": user_id, "amount": amount}
    except Exception as e:
        # Повтор через 60 секунд
        self.retry(exc=e, countdown=60)

@app.task
def generate_report(user_id: int):
    """Генерация отчёта (долгая операция)"""
    print(f"Generating report for user {user_id}")
    return {"report_url": f"/reports/{user_id}.pdf"}
