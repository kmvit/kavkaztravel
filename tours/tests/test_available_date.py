import pytest
from django.utils import timezone
from rest_framework import status
from tours.models import AvailableDateTour
from datetime import timedelta

TODAY = timezone.now().date()
FUTURE_START = TODAY.replace(day=TODAY.day + 1)
FUTURE_END = TODAY + timedelta(days=10)
PAST_START = TODAY - timedelta(days=10)
PAST_END = TODAY.replace(day=TODAY.day - 1)

AVAILABLE_DATE_URL = "/api/v1/tours/available_dates/"


@pytest.mark.django_db
def test_create_available_date(api_client, tour):
    """Создание доступной даты тура."""
    payload = {
        "tour": tour.id,
        "start_date": str(FUTURE_START),
        "end_date": str(FUTURE_END),
        "is_active": True,
    }
    response = api_client.post(AVAILABLE_DATE_URL, data=payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert AvailableDateTour.objects.count() == 1


@pytest.mark.django_db
def test_get_available_date_list(api_client, available_date_tour):
    """Получение списка доступных дат туров."""
    response = api_client.get(AVAILABLE_DATE_URL)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["id"] == available_date_tour.id


@pytest.mark.django_db
def test_update_available_date(api_client, available_date_tour):
    """Обновление существующей даты тура."""
    url = f"{AVAILABLE_DATE_URL}{available_date_tour.id}/"
    response = api_client.patch(url, data={"is_active": False})
    assert response.status_code == status.HTTP_200_OK
    available_date_tour.refresh_from_db()
    assert available_date_tour.is_active is False


@pytest.mark.django_db
def test_delete_available_date(api_client, available_date_tour):
    """Удаление доступной даты тура."""
    url = f"{AVAILABLE_DATE_URL}{available_date_tour.id}/"
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert AvailableDateTour.objects.count() == 0


@pytest.mark.django_db
def test_end_date_before_start_date(api_client, tour):
    """Дата окончания не может быть раньше даты начала."""
    payload = {
        "tour": tour.id,
        "start_date": str(FUTURE_END),
        "end_date": str(FUTURE_START),
        "is_active": True,
    }
    response = api_client.post(AVAILABLE_DATE_URL, data=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = response.json()
    assert "end_date" in response_data
    assert "должна быть позже даты начала" in response_data["end_date"][0].lower()


@pytest.mark.django_db
def test_start_date_in_past(api_client, tour):
    """Дата начала не может быть в прошлом."""
    payload = {
        "tour": tour.id,
        "start_date": str(PAST_START),
        "end_date": str(FUTURE_END),
        "is_active": True,
    }
    response = api_client.post(AVAILABLE_DATE_URL, data=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "start_date" in response.json()  # Проверяем что ошибка привязана к полю
    assert (
        "не может быть в прошлом" in response.json()["start_date"][0]
    )  # Проверяем текст ошибки


@pytest.mark.django_db
def test_end_date_in_past(api_client, tour):
    """Дата окончания не может быть в прошлом."""
    payload = {
        "tour": tour.id,
        "start_date": str(FUTURE_START),
        "end_date": str(PAST_END),
        "is_active": True,
    }
    response = api_client.post(AVAILABLE_DATE_URL, data=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "end_date" in response.json()  # Проверяем что ошибка привязана к полю
    assert (
        "не может быть в прошлом" in response.json()["end_date"][0]
    )  # Проверяем текст ошибки


@pytest.mark.django_db
def test_only_future_dates_are_returned(api_client, tour):
    """В списке отображаются только будущие даты."""
    # Создаём прошедшую дату
    AvailableDateTour.objects.create(
        tour=tour, start_date=PAST_START, end_date=PAST_END, is_active=True
    )
    # И будущую
    AvailableDateTour.objects.create(
        tour=tour, start_date=FUTURE_START, end_date=FUTURE_END, is_active=True
    )

    response = api_client.get(AVAILABLE_DATE_URL)
    assert response.status_code == status.HTTP_200_OK
    # Ожидаем только одну дату — будущую
    assert len(response.data) == 1
    assert response.data[0]["start_date"] == str(FUTURE_START)
