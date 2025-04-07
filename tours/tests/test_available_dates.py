import pytest
from rest_framework import status
from tours.models import AvailableDateTour
# tests/test_available_dates.py
import pytest
from datetime import date, timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
from rest_framework import status
# tests/test_available_dates.py
import pytest
from datetime import date, timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
from rest_framework import status

API_URL = "/api/v1/tours/available_dates/"



# CRUD Tests
@pytest.mark.django_db
def test_create_available_date(api_client, valid_date_data):
    """Создание нового периода"""
    response = api_client.post(API_URL, valid_date_data, format='json')
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["start_date"] == str(valid_date_data["start_date"])
    assert response.data["duration"] == 2

@pytest.mark.django_db
def test_retrieve_available_date(api_client, available_date_tour):
    """Получение периода по ID"""
    response = api_client.get(f"{API_URL}{available_date_tour.id}/")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data["tour"] == available_date_tour.tour.id
    assert response.data["is_active"] is True

@pytest.mark.django_db
def test_update_available_date(api_client, user, available_date_tour):
    """Полное обновление периода"""
    api_client.force_authenticate(user=user)
    update_data = {
        "tour": available_date_tour.tour.id,
        "start_date": date.today() + timedelta(days=10),
        "end_date": date.today() + timedelta(days=12),
        "is_active": False
    }
    response = api_client.put(
        f"{API_URL}{available_date_tour.id}/", 
        update_data, 
        format='json'
    )
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data["is_active"] is False


@pytest.mark.django_db
def test_delete_available_date(api_client, user, available_date_tour):
    """Удаление периода"""
    api_client.force_authenticate(user=user)
    response = api_client.delete(f"{API_URL}{available_date_tour.id}/")
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = api_client.get(f"{API_URL}{available_date_tour.id}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND

# Validation Tests
@pytest.mark.django_db
def test_past_start_date_validation(api_client, user, tour):
    """Дата начала в прошлом"""
    api_client.force_authenticate(user=user)
    invalid_data = {
        "tour": tour.id,
        "start_date": date.today() - timedelta(days=1),
        "end_date": date.today() + timedelta(days=1)
    }
    response = api_client.post(API_URL, invalid_data, format='json')
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "начала тура" in response.data["non_field_errors"][0]

@pytest.mark.django_db
def test_end_before_start_validation(api_client, user, valid_date_data):
    """Дата окончания раньше начала"""
    api_client.force_authenticate(user=user)
    invalid_data = {**valid_date_data, "end_date": valid_date_data["start_date"]}
    response = api_client.post(API_URL, invalid_data, format='json')
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "окончания тура" in response.data["non_field_errors"][0]

@pytest.mark.django_db
def test_overlapping_dates_validation(api_client, user, available_date_tour):
    """Пересечение периодов"""
    api_client.force_authenticate(user=user)
    overlapping_data = {
        "tour": available_date_tour.tour.id,
        "start_date": available_date_tour.start_date + timedelta(days=1),
        "end_date": available_date_tour.end_date + timedelta(days=1)
    }
    response = api_client.post(API_URL, overlapping_data, format='json')
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "пересекаются" in response.data["non_field_errors"][0]


# Business Logic Tests
@pytest.mark.django_db
def test_duration_calculation(available_date_tour):
    """Расчет продолжительности"""
    assert available_date_tour.duration.days == 3

@pytest.mark.django_db
def test_auto_deactivation(api_client, user, available_date_tour):
    """Автодеактивация прошедших дат"""
    old_date = AvailableDateTour.objects.create(
        tour=available_date_tour.tour,
        start_date=date.today() - timedelta(days=10),
        end_date=date.today() - timedelta(days=5),
        is_active=True
    )
    
    AvailableDateTour.objects.deactivate_past_dates()
    old_date.refresh_from_db()
    
    assert old_date.is_active is False
    assert available_date_tour.is_active is True

# Relations Tests
@pytest.mark.django_db
def test_cascade_delete(api_client, user, tour, available_date_tour):
    """Каскадное удаление с туром"""
    api_client.force_authenticate(user=user)
    response = api_client.delete(f"/api/v1/tours/{tour.id}/")
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = api_client.get(f"{API_URL}{available_date_tour.id}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
