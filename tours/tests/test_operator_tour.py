import pytest
from rest_framework import status
from tours.models import TourOperator

TOUR_OPERATOR_URL = "/api/v1/tours/touroperators/"


@pytest.fixture
def tour_operator_data(child_region, owner):
    """Данные для создания туроператора."""
    return {
        "region": child_region.id,
        "license_number": "TO-123456",
        "name": "Лучший туроператор",
        "url": "best-tour-operator",
        "description": "Описание туроператора",
        "content": "Подробное описание",
        "seo_title": "SEO заголовок",
        "seo_description": "SEO описание",
    }


def test_create_touroperator_by_owner(api_client, owner, tour_operator_data):
    """Тест создания туроператора владельцем."""
    api_client.force_authenticate(user=owner)
    response = api_client.post(TOUR_OPERATOR_URL, tour_operator_data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert TourOperator.objects.count() == 1
    assert TourOperator.objects.get().license_number == "TO-123456"


def test_list_touroperators(api_client, tour_operator):
    """Тест получения списка туроператоров."""
    response = api_client.get(TOUR_OPERATOR_URL)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["license_number"] == tour_operator.license_number


def test_retrieve_touroperator(api_client, tour_operator):
    """Тест получения одного туроператора."""
    url = f"{TOUR_OPERATOR_URL}{tour_operator.id}/"
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["license_number"] == tour_operator.license_number


def test_update_touroperator_by_owner(api_client, owner, tour_operator):
    """Тест обновления туроператора владельцем."""
    api_client.force_authenticate(user=owner)
    url = f"{TOUR_OPERATOR_URL}{tour_operator.id}/"
    updated_data = {"license_number": "TO-999999"}
    response = api_client.patch(url, updated_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    tour_operator.refresh_from_db()
    assert tour_operator.license_number == "TO-999999"


def test_delete_touroperator_by_owner(api_client, owner, tour_operator):
    """Тест удаления туроператора владельцем."""
    api_client.force_authenticate(user=owner)
    url = f"{TOUR_OPERATOR_URL}{tour_operator.id}/"
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert TourOperator.objects.count() == 0
