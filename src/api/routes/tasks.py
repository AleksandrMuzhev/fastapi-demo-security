# src/api/routes/tasks.py
from fastapi import APIRouter
from pydantic import BaseModel
from src.tasks.tasks import send_email, process_payment, generate_report
from celery.result import AsyncResult

router = APIRouter(prefix="/tasks", tags=["tasks"])

class EmailRequest(BaseModel):
    email: str
    subject: str
    body: str

class PaymentRequest(BaseModel):
    user_id: int
    amount: int

@router.post("/send-email")
async def send_email_endpoint(data: EmailRequest):
    # Запускаем задачу в фоне
    task = send_email.delay(
        email=data.email,
        subject=data.subject,
        body=data.body
    )
    return {"task_id": task.id, "status": "queued"}

@router.post("/process-payment")
async def process_payment_endpoint(data: PaymentRequest):
    task = process_payment.delay(
        user_id=data.user_id,
        amount=data.amount
    )
    return {"task_id": task.id, "status": "processing"}

@router.get("/status/{task_id}")
async def get_task_status(task_id: str):
    result = AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None
    }
