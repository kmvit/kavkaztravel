import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from kashiring.models import Car, CarFeature, CarImage, RentalDiscount, RentalCondition
from datetime import datetime, timedelta

User = get_user_model()


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
    """Фикстура для создания тестовой скидки."""
    return RentalDiscount.objects.create(
        name="123", discount_week=5.00, discount_month=10.00
    )


@pytest.fixture
def car_1(db, user, rental_discount):
    """Фикстура для создания первого тестового автомобиля."""
    return Car.objects.create(
        owner=user,
        brand="kia",
        body_type="sedan",
        price_per_day=100,
        discount_policy=rental_discount,
    )


@pytest.fixture
def car_2(db, user):
    """Фикстура для создания второго тестового автомобиля без скидки."""
    return Car.objects.create(
        owner=user,
        brand="toyota",
        body_type="sedan",
        price_per_day=6100,
        discount_policy=None,
    )


@pytest.fixture
def car_1_features(db, car_1):
    """Фикстура для характеристик первого автомобиля."""
    return [
        CarFeature.objects.create(car=car_1, name="air_conditioning"),
        CarFeature.objects.create(car=car_1, name="four_doors"),
    ]


@pytest.fixture
def car_2_features(db, car_2):
    """Фикстура для характеристики второго автомобиля."""
    return [
        CarFeature.objects.create(car=car_2, name="air_conditioning"),
    ]


@pytest.fixture
def car_1_images(db, car_1):
    """Фикстура для изображений первого автомобиля."""
    return [
        CarImage.objects.create(car=car_1, image="car_images/endpoint.png"),
        CarImage.objects.create(car=car_1, image="car_images/db.png"),
    ]


@pytest.fixture
def car_2_images(db, car_2):
    """Фикстура для изображений второго автомобиля (пустой список)."""
    return []


@pytest.fixture
def rental_condition(db, car_1):
    """Фикстура для создания тестовых условий аренды."""
    return RentalCondition.objects.create(
        car=car_1,
        insurance_deposit=-7316.81,
        required_documents="Passport, Driver's License",
        min_driver_age=21,
        min_driving_experience=2,
    )


@pytest.fixture
def rental_payload(car_1, user):
    """Фикстура с данными для создания аренды."""
    return {
        "car": car_1.id,
        "renter": user.id,
        "user": user.id,  # Добавляем user
        "pickup_datetime": "2025-03-20T14:22:59.765000Z",  # Добавляем pickup
        "return_datetime": "2025-03-28T14:22:59.765000Z",  # Добавляем return
        "daily_price": "100.00",  # Добавляем цену за день
    }


@pytest.fixture
def rental_payload2(car_1, user):
    """Фикстура с данными для создания аренды."""
    return {
        "car": car_1.id,
        "renter": user.id,
        "user": user.id,  # Добавляем user
        "pickup_datetime": "2025-03-28T14:22:59.765000Z",  # Добавляем pickup
        "return_datetime": "2025-04-28T14:22:59.765000Z",  # Добавляем return
        "daily_price": "100.00",  # Добавляем цену за день
    }
