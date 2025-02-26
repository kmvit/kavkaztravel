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

    payload = {"brand": "toyota", "price_per_day": 500.00}  # Убрал кавычки вокруг числа

    response = api_client.patch(url, payload, format="json")

    print(response.status_code, response.json())  # Выводим статус и тело ответа

    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_car(api_client, user, car_1):
    """Тест удаления автомобиля через API."""
    api_client.force_authenticate(user=user)

    url = f"/api/v1/kashiring/cars/{car_1.id}/"  # Прямой URL
  
    response = api_client.delete(url)

    assert response.status_code == 204
    assert not Car.objects.filter(id=car_1.id).exists()
