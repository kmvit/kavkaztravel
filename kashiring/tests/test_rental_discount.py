import pytest
from kashiring.models import RentalDiscount

@pytest.mark.django_db
def test_get_discounts(api_client, rental_discount):
    """Тест получения списка скидок."""
    url = "/api/v1/kashiring/discounts/"  # Прямая ссылка
    response = api_client.get(url)

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "123"


@pytest.mark.django_db
def test_create_discount(api_client):
    """Тест создания новой скидки."""
    url = "/api/v1/kashiring/discounts/"  # Прямая ссылка
    payload = {
        "name": "New Discount",
        "discount_week": "7.50",
        "discount_month": "15.00"
    }

    response = api_client.post(url, payload, format="json")

    assert response.status_code == 201
    assert response.json()["name"] == "New Discount"


@pytest.mark.django_db
def test_update_discount(api_client, rental_discount):
    """Тест обновления скидки."""
    url = f"/api/v1/kashiring/discounts/{rental_discount.id}/"  # Прямая ссылка
    payload = {"discount_week": "8.00"}

    response = api_client.patch(url, payload, format="json")

    assert response.status_code == 200
    assert response.json()["discount_week"] == "8.00"


@pytest.mark.django_db
def test_delete_discount(api_client, rental_discount):
    """Тест удаления скидки."""
    url = f"/api/v1/kashiring/discounts/{rental_discount.id}/"  # Прямая ссылка
    response = api_client.delete(url)

    assert response.status_code == 204
    assert RentalDiscount.objects.filter(id=rental_discount.id).exists() is False


@pytest.mark.django_db
@pytest.mark.parametrize(
    "days, expected_discount",
    [
        (1, 0),       # Меньше 7 дней → скидки нет
        (7, 0.05),    # От 7 дней → 5%
        (30, 0.10),   # От 30 дней → 10%
        (100, 0.10),  # Дольше 30 дней → 10%
    ]
)
def test_get_discount(rental_discount, days, expected_discount):
    """Тест метода get_discount."""
    assert rental_discount.get_discount(days) == expected_discount
