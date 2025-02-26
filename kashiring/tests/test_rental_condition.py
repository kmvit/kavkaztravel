import pytest
from django.urls import reverse
from kashiring.models import RentalCondition
from datetime import datetime, timedelta

import pytest
from django.utils import timezone
from datetime import datetime

@pytest.mark.django_db
def test_get_rental_conditions(api_client, rental_condition):
    """Тест получения списка условий аренды."""
    url = "/api/v1/kashiring/rental-conditions/"
    response = api_client.get(url)

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["car"] == rental_condition.car.id


@pytest.mark.django_db
def test_create_rental_condition(api_client, car_2):
    """Тест создания условий аренды."""
    url = "/api/v1/kashiring/rental-conditions/"
    payload = {
        "car": car_2.id,
        "insurance_deposit": "1000.00",
        "required_documents": "ID, Driving License",
        "min_driver_age": 25,
        "min_driving_experience": 3,
        "rental_start_date": timezone.make_aware(datetime(2025, 2, 26, 14, 22, 59, 765000)).isoformat(),
        "rental_end_date": timezone.make_aware(datetime(2025, 3, 5, 14, 22, 59, 765000)).isoformat(),
    }

    response = api_client.post(url, payload, format="json")

    assert response.status_code == 201
    assert response.json()["min_driver_age"] == 25


@pytest.mark.django_db
def test_update_rental_condition(api_client, rental_condition):
    """Тест обновления условий аренды."""
    url = f"/api/v1/kashiring/rental-conditions/{rental_condition.id}/"
    payload = {"min_driver_age": 23}

    response = api_client.patch(url, payload, format="json")

    assert response.status_code == 200
    assert response.json()["min_driver_age"] == 23
