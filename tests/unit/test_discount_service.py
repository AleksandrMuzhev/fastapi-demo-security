# tests/unit/test_discount_service.py
import pytest
from src.services.discount_service import DiscountService


def test_discount_for_member():
    service = DiscountService()
    assert service.calculate_discount(age=25, is_member=True) == 15


def test_discount_for_senior():
    service = DiscountService()
    assert service.calculate_discount(age=65, is_member=False) == 10


def test_discount_for_regular():
    service = DiscountService()
    assert service.calculate_discount(age=25, is_member=False) == 0


@pytest.mark.parametrize("age, is_member, expected", [
    (25, True, 15),
    (65, False, 10),
    (25, False, 0),
    (18, True, 15),
])
def test_discount_parametrized(age, is_member, expected):
    service = DiscountService()
    assert service.calculate_discount(age, is_member) == expected
