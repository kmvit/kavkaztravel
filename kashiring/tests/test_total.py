import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from kashiring.models import Rental, RentalDiscount, Car



@pytest.fixture
def api_client():
    """Фикстура для API клиента."""
    return APIClient()


@pytest.fixture
def user(db):
    """Фикстура для создания тестового пользователя."""
    return User.objects.create_user(username="anton", password="testpassword")


@pytest.fixture
def rental_discount(db):
    """Фикстура для скидки на аренду."""
    return RentalDiscount.objects.create(name="Standard", discount_week=5.00, discount_month=10.00)


@pytest.fixture
def car(db, user, rental_discount):
    """Фикстура для автомобиля с ценой и скидкой."""
    return Car.objects.create(
        owner=user,
        brand="Toyota",
        body_type="sedan",
        price_per_day=1000.00,
        discount_policy=rental_discount
    )


@pytest.fixture
def rental_payload(car, user):
    """Фикстура с данными для создания аренды (9 дней)."""
    return {
        "car": car.id,
        "renter": user.id,
        "rental_start_date": "2025-02-26T14:22:59.765000Z",
        "rental_end_date": "2025-03-06T14:22:59.765000Z"  # 9 дней аренды
    }

@pytest.mark.django_db
def test_create_rental_with_discount(api_client, rental_payload, rental_discount):
    """Проверяем, что при аренде от 7 дней применяется недельная скидка."""
    cd kurl = "/api/v1/kashiring/rental/create/"  # Используем прямой URL
    response = api_client.post(url, rental_payload, format="json")

    assert response.status_code == 201
    data = response.json()
    
    assert "rental_id" in data
    assert "total_price" in data
    
    # Расчет ожидаемой стоимости
    expected_discount = rental_discount.discount_week / 100  # 5% скидки
    expected_price = 1000 * 9 * (1 - expected_discount)  # 9 дней аренды со скидкой

    assert float(data["total_price"]) == pytest.approx(expected_price, rel=1e-2)
