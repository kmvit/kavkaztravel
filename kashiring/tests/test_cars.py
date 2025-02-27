import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from kashiring.models import Car, CarFeature, CarImage, RentalDiscount

import pytest
from django.urls import reverse
from kashiring.models import Car, CarFeature
import pytest
from django.urls import reverse
from kashiring.models import Car, CarFeature


@pytest.mark.django_db
def test_create_car(api_client, user, rental_discount):
    """Тест создания автомобиля через API."""
    api_client.force_authenticate(user=user)

    url = "/api/v1/kashiring/cars/"  # Прямой URL без reverse()
    payload = {
        "owner": user.id,
        "brand": "toyota",
        "body_type": "sedan",
        "price_per_day": "47466.43",
        "features": [{"name": "air_conditioning"}],
        "discount_policy": rental_discount.name,
    }

    response = api_client.post(url, payload, format="json")
    assert response.status_code == 201

    data = response.json()
    assert data["brand"] == "toyota"
    assert data["features"][0]["name"] == "air_conditioning"

    car = Car.objects.get(id=data["id"])
    assert car.brand == "toyota"
    assert CarFeature.objects.filter(car=car, name="air_conditioning").exists()


@pytest.mark.django_db
def test_update_car(api_client, user, car_1):
    """Тест обновления автомобиля через API."""
    api_client.force_authenticate(user=user)

    url = f"/api/v1/kashiring/cars/{car_1.id}/"

    payload = {"brand": "toyota", "price_per_day": 500.00}

    response = api_client.patch(url, payload, format="json")

    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_car(api_client, user, car_1):
    """Тест удаления автомобиля через API."""
    api_client.force_authenticate(user=user)

    url = f"/api/v1/kashiring/cars/{car_1.id}/"

    response = api_client.delete(url)

    assert response.status_code == 204
    assert not Car.objects.filter(id=car_1.id).exists()


@pytest.mark.django_db
def test_filter_cars_by_brand(api_client, car_1, car_2):
    """Фильтрация автомобилей по бренду."""
    url = "/api/v1/kashiring/cars/?brand=kia"
    response = api_client.get(url)

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["brand"] == "kia"


@pytest.mark.django_db
def test_filter_cars_by_body_type(api_client, car_1, car_2):
    """Фильтрация автомобилей по типу кузова."""
    url = "/api/v1/kashiring/cars/?body_type=sedan"
    response = api_client.get(url)

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2  # Оба авто - седаны


@pytest.mark.django_db
def test_filter_cars_by_price_range(api_client, car_1, car_2):
    """Фильтрация автомобилей по диапазону цены."""
    url = "/api/v1/kashiring/cars/?price_per_day_min=50&price_per_day_max=500"
    response = api_client.get(url)

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert float(data[0]["price_per_day"]) == 100.00


@pytest.mark.django_db
def test_filter_cars_by_features(
    api_client, car_1, car_2, car_1_features, car_2_features
):
    """Фильтрация автомобилей по характеристикам (например, кондиционер)."""
    url = "/api/v1/kashiring/cars/?features=air_conditioning"
    response = api_client.get(url)

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2  # Оба авто имеют кондиционер


import pytest
from rest_framework import status
from kashiring.models import Car


@pytest.mark.django_db
def test_anonymous_user_cannot_edit_car(api_client, car_1):
    """Неавторизованный пользователь не может редактировать машину."""
    url = f"/api/v1/kashiring/cars/{car_1.id}/"
    data = {"brand": "Honda"}  # Пробуем изменить бренд

    response = api_client.patch(url, data, format="json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED  # Ожидаем 401 ошибку
    car_1.refresh_from_db()
    assert car_1.brand != "Honda"  # Убеждаемся, что данные не изменились
