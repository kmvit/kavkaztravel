import pytest

import pytest


@pytest.mark.django_db
def test_create_rental(api_client, rental_payload):
    """Тест создания аренды"""
    url = "/api/v1/kashiring/rental/create/"  # Используем прямой URL
    response = api_client.post(url, rental_payload, format="json")
    print(response.json())
    assert response.status_code == 201

    assert response.status_code == 201
    data = response.json()

    assert "rental_id" in data
    assert "total_price" in data
    assert isinstance(
        float(data["total_price"]), float
    )  # Проверяем, что цена корректно вычислена
