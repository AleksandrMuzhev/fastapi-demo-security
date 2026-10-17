# src/services/discount_service.py
class DiscountService:
    def calculate_discount(self, age: int, is_member: bool) -> int:
        """Рассчитывает скидку в процентах"""
        if is_member:
            return 15
        if age > 60:
            return 10
        return 0
