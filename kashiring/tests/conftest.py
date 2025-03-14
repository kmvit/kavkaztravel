import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from kashiring.models import (
    Car,
    CarFeature,
    CarImage,
    RentalDiscount,
    RentalCondition,
    Brand,
    Model,
    CarOption,
    CarEquipment,
)
from datetime import datetime, timedelta

User = get_user_model()


@pytest.fixture
def api_client():
    """Фикстура для API клиента."""
    return APIClient()


# Фикстура для владельца машины
@pytest.fixture
def owner(db):
    """Фикстура для пользователя-владельца."""
    User = get_user_model()
    return User.objects.create_user(
        username="owner_user", password="password123", email="owner@example.com"
    )


# Фикстура для арендатора (не владельца)
@pytest.fixture
def user(db):
    """Фикстура для пользователя, не являющегося владельцем машины."""
    User = get_user_model()
    return User.objects.create_user(
        username="renter_user", password="password123", email="renter@example.com"
    )


@pytest.fixture
def rental_discount(db):
    """Фикстура для создания тестовой скидки (неделя + месяц)."""
    return RentalDiscount.objects.create(
        name="123", discount_week=5.00, discount_month=10.00
    )


@pytest.fixture
def rental_discount_none(db):
    """Фикстура для аренды без скидки."""
    return RentalDiscount.objects.create(
        name="No Discount", discount_week=0.00, discount_month=0.00
    )


@pytest.fixture
def brand_kia(db):
    return Brand.objects.create(name="Kia")


@pytest.fixture
def brand_toyota(db):
    return Brand.objects.create(name="Toyota")


@pytest.fixture
def model_rio(db, brand_kia):
    return Model.objects.create(name="Rio")


@pytest.fixture
def model_camry(db, brand_toyota):
    return Model.objects.create(name="Camry")


@pytest.fixture
def car_option_1(car_1):
    """Фикстура для дополнительной опции автомобиля."""
    option = CarOption.objects.create(car=car_1, name="Leather Seats", price=500.00)
    return option


@pytest.fixture
def car_equipment_1(car_1):
    """Фикстура для комплектации автомобиля."""
    equipment = CarEquipment.objects.create(car=car_1, name="Premium Sound System")
    return equipment


@pytest.fixture
def car_1(db, owner, rental_discount, model_rio, brand_kia):
    """Фикстура для создания первого тестового автомобиля с заданным тарифом и моделью."""
    return Car.objects.create(
        owner=owner,
        brand=brand_kia,
        model=model_rio,
        description="Не совсем комфортый седан",
        body_type="sedan",
        year_of_production=2022,
        engine_power=123,
        drive_type="fwd",
        engine_type="petrol",
        price_per_day=100,
        discount_policy=rental_discount,
    )


@pytest.fixture
def car_2(db, owner, model_camry, brand_toyota):
    """Фикстура для создания второго тестового автомобиля без скидки."""
    return Car.objects.create(
        owner=owner,
        brand=brand_toyota,
        model=model_camry,
        description="Бизнес-седан",
        body_type="sedan",
        year_of_production=2021,
        engine_power=249,
        drive_type="fwd",
        engine_type="petrol",
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


import pytest
from datetime import datetime, timedelta


@pytest.fixture
def rental_payload_less_than_7_days(car_1, user):
    """Фикстура для аренды на меньше чем 7 дней."""
    return {
        "car": car_1.id,
        "renter": user.id,
        "user": user.id,
        "pickup_datetime": "2025-03-20T14:22:59.765000Z",
        "return_datetime": "2025-03-24T14:22:59.765000Z",  # Аренда на 4 дня
    }


@pytest.fixture
def rental_payload_7_days(car_1, user):
    """Фикстура для аренды на 7 дней."""
    return {
        "car": car_1.id,
        "renter": user.id,
        "user": user.id,
        "pickup_datetime": "2025-03-20T14:22:59.765000Z",
        "return_datetime": "2025-03-27T14:22:59.765000Z",  # Аренда на 7 дней
    }


@pytest.fixture
def rental_payload_between_7_and_30_days(car_1, user):
    """Фикстура для аренды от 7 до 30 дней."""
    return {
        "car": car_1.id,
        "renter": user.id,
        "user": user.id,
        "pickup_datetime": "2025-03-20T14:22:59.765000Z",
        "return_datetime": "2025-04-10T14:22:59.765000Z",  # Аренда на 21 день
    }


@pytest.fixture
def rental_payload_30_days(car_1, user):
    """Фикстура для аренды на 30 дней."""
    return {
        "car": car_1.id,
        "renter": user.id,
        "user": user.id,
        "pickup_datetime": "2025-03-20T14:22:59.765000Z",
        "return_datetime": "2025-04-20T14:22:59.765000Z",  # Аренда на 30 дней
    }


@pytest.fixture
def rental_payload_more_than_30_days(car_1, user):
    """Фикстура для аренды больше 30 дней."""
    return {
        "car": car_1.id,
        "renter": user.id,
        "user": user.id,
        "pickup_datetime": "2025-03-20T14:22:59.765000Z",
        "return_datetime": "2025-05-10T14:22:59.765000Z",  # Аренда на 51 день
    }


@pytest.fixture
def rental_discount(db):
    """Фикстура для создания тестовой скидки (неделя + месяц)."""
    return RentalDiscount.objects.create(
        name="123", discount_week=5.00, discount_month=10.00
    )


@pytest.fixture
def rental_discount_none(db):
    """Фикстура для аренды без скидки."""
    return RentalDiscount.objects.create(
        name="No Discount", discount_week=0.00, discount_month=0.00
    )


@pytest.fixture
def rental_payload_less_than_7_days(car_1, rental_discount):
    """Фикстура для аренды меньше 7 дней с заданными параметрами."""
    pickup_datetime = datetime.utcnow()
    return {
        "car": car_1.id,
        "discount_policy": rental_discount.id,
        "pickup_datetime": pickup_datetime.isoformat(),
        "return_datetime": (pickup_datetime + timedelta(days=5)).isoformat(),
        "return_location": "Some location",
    }


@pytest.fixture
def rental_payload_7_days(car_1, rental_discount):
    """Фикстура для аренды на 7 дней с заданными параметрами."""
    pickup_datetime = datetime.utcnow()
    return {
        "car": car_1.id,
        "discount_policy": rental_discount.id,
        "pickup_datetime": pickup_datetime.isoformat(),
        "return_datetime": (pickup_datetime + timedelta(days=7)).isoformat(),
        "return_location": "Some location",
    }


@pytest.fixture
def rental_payload_between_7_and_30_days(car_1, rental_discount):
    """Фикстура для аренды между 7 и 30 днями с заданными параметрами."""
    pickup_datetime = datetime.utcnow()
    return {
        "car": car_1.id,
        "discount_policy": rental_discount.id,
        "pickup_datetime": pickup_datetime.isoformat(),
        "return_datetime": (pickup_datetime + timedelta(days=15)).isoformat(),
        "return_location": "Some location",
    }


@pytest.fixture
def rental_payload_30_days(car_1, rental_discount):
    """Фикстура для аренды на 30 дней с заданными параметрами."""
    pickup_datetime = datetime.utcnow()
    return {
        "car": car_1.id,
        "discount_policy": rental_discount.id,
        "pickup_datetime": pickup_datetime.isoformat(),
        "return_datetime": (pickup_datetime + timedelta(days=30)).isoformat(),
        "return_location": "Some location",
    }


@pytest.fixture
def rental_payload_more_than_30_days(car_1, rental_discount):
    """Фикстура для аренды больше 30 дней с заданными параметрами."""
    pickup_datetime = datetime.utcnow()
    return {
        "car": car_1.id,
        "discount_policy": rental_discount.id,
        "pickup_datetime": pickup_datetime.isoformat(),
        "return_datetime": (pickup_datetime + timedelta(days=45)).isoformat(),
        "return_location": "Some location",
    }
