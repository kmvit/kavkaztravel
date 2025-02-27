import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from kashiring.models import Rental, RentalDiscount, Car


@pytest.mark.django_db
def test_create_rental_with_discount(api_client, rental_payload, rental_discount):
    """Проверяем, что при аренде от 7 дней применяется недельная скидка."""
    url = "/api/v1/kashiring/rental/create/"  # Используем прямой URL
    response = api_client.post(url, rental_payload, format="json")
    assert response.status_code == 201
    data = response.json()

    assert "rental_id" in data
    assert "total_price" in data

    # Расчет ожидаемой стоимости
    expected_discount = rental_discount.discount_week / 100  # 10% скидки
    print(f"{expected_discount} - expected_discount")
    expected_price = 100 * 8 * (1 - expected_discount)  # 9 дней аренды со скидкой
    print(f"{expected_price} - expected_price")
    assert float(data["total_price"]) == expected_price


@pytest.mark.django_db
def test_create_rental_with_discount2(api_client, rental_payload2, rental_discount):
    """Проверяем, что при аренде от 30 дней применяется месячная скидка."""
    url = "/api/v1/kashiring/rental/create/"  # Используем прямой URL
    response = api_client.post(url, rental_payload2, format="json")
    print(response.json())
    assert response.status_code == 201
    data = response.json()

    assert "rental_id" in data
    assert "total_price" in data

    # Расчет ожидаемой стоимости
    expected_discount = rental_discount.discount_month / 100  # 10% скидки
    print(f"{expected_discount} - expected_discount")
    expected_price = 100 * 31 * (1 - expected_discount)  # 9 дней аренды со скидкой
    print(f"{expected_price} - expected_price")
    assert float(data["total_price"]) == expected_price
