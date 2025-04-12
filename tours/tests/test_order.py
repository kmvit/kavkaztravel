import pytest
from rest_framework import status
from datetime import date, timedelta
from django.contrib.auth import get_user_model
from tours.models import Order

URL = "/api/v1/tours/order/"


# Тесты CREATE
def test_create_order_success(api_client, tour):
    """Успешное создание заказа"""
    data = {
        "tour": tour.id,
        "date": (date.today() + timedelta(days=10)).isoformat(),
        "size": 3,
        "username": "test_user",
        "email": "test@example.com",
        "phone": "+71234567890",
    }
    response = api_client.post(URL, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["tour"] == tour.id
    assert "owner" not in response.data


def test_retrieve_order(api_client, order):
    """Получение деталей заказа"""
    response = api_client.get(f"{URL}{order.id}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == order.id
    assert response.data["username"] == order.username


def test_list_orders(api_client, order):
    """Получение списка заказов"""
    response = api_client.get(URL)
    assert response.status_code == status.HTTP_200_OK
    assert any(o["id"] == order.id for o in response.data)


def test_update_order(api_client, order):
    """Обновление заказа"""
    response = api_client.patch(
        f"{URL}{order.id}/", {"size": 5, "email": "updated@example.com"}
    )

    assert response.status_code == status.HTTP_200_OK
    order.refresh_from_db()
    assert order.size == 5
    assert order.email == "updated@example.com"


def test_delete_order(api_client, order):
    """Удаление заказа"""
    response = api_client.delete(f"{URL}{order.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Order.objects.filter(id=order.id).exists()


def test_invalid_phone_format(api_client, tour):
    """Неверный формат телефона"""
    response = api_client.post(
        URL,
        {
            "tour": tour.id,
            "date": (date.today() + timedelta(days=5)).isoformat(),
            "size": 2,
            "username": "test",
            "phone": "12345",  # Неверный формат
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "phone" in response.data
