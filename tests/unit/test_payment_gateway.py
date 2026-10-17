# tests/unit/test_payment_gateway.py
import pytest
from unittest.mock import AsyncMock
from src.services.payment_gateway import PaymentGateway


@pytest.mark.asyncio
async def test_payment_with_mock():
    # Создаём мок
    gateway = PaymentGateway()
    gateway.charge = AsyncMock(return_value={
        "status": "success",
        "transaction_id": "txn_123"
    })

    # Вызываем
    result = await gateway.charge(1000, {"number": "4111...", "cvv": "123"})

    # Проверяем
    assert result["status"] == "success"
    assert result["transaction_id"] == "txn_123"

    # Проверяем, что метод был вызван с правильными аргументами
    gateway.charge.assert_called_once_with(1000, {"number": "4111...", "cvv": "123"})
