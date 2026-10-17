# src/services/payment_gateway.py
class PaymentGateway:
    async def charge(self, amount: int, card_data: dict) -> dict:
        # Реальный запрос к внешнему API
        # ...
        pass