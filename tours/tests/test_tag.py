import pytest
from rest_framework.test import APIClient
from rest_framework import status
from tours.models import TagTour

BASE_URL = "/api/v1/tours/tag/"


@pytest.mark.django_db
def test_tag_list(api_client, tag):
    """Проверка получения списка тегов."""
    response = api_client.get(BASE_URL)
    assert response.status_code == status.HTTP_200_OK
    assert any(t["name"] == tag.name for t in response.data)


@pytest.mark.django_db
def test_tag_detail(api_client, tag):
    """Проверка получения одного тега по ID."""
    response = api_client.get(f"{BASE_URL}{tag.id}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == tag.name


@pytest.mark.django_db
def test_tag_create(api_client):
    """Проверка создания нового тега."""
    data = {
        "name": "Экскурсия",
        "description": "Групповая экскурсия по городу",
        "tag_type": "Тип 2",
    }
    response = api_client.post(BASE_URL, data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert TagTour.objects.filter(name="Экскурсия").exists()


@pytest.mark.django_db
def test_tag_create_unique_constraint(api_client, tag):
    """Проверка ошибки при создании тега с неуникальным именем."""
    data = {
        "name": tag.name,  # уже существует
        "description": "Дублирующий тег",
        "tag_type": "Тип 1",
    }
    response = api_client.post(BASE_URL, data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "name" in response.data


@pytest.mark.django_db
def test_tag_update(api_client, tag):
    """Проверка обновления существующего тега."""
    data = {
        "name": "Обновленный тег",
        "description": tag.description,
        "tag_type": tag.tag_type,
    }
    response = api_client.put(f"{BASE_URL}{tag.id}/", data=data)
    assert response.status_code == status.HTTP_200_OK
    tag.refresh_from_db()
    assert tag.name == "Обновленный тег"


@pytest.mark.django_db
def test_tag_delete(api_client, tag):
    """Проверка удаления тега."""
    response = api_client.delete(f"{BASE_URL}{tag.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not TagTour.objects.filter(id=tag.id).exists()


@pytest.mark.django_db
def test_tag_create_minimal_fields(api_client):
    """
    Проверка создания тега только с обязательным полем `name`,
    без описания и типа тега.
    """
    data = {
        "name": "Минимальный тег"
        # description и tag_type отсутствуют
    }
    response = api_client.post(BASE_URL, data=data)
    assert response.status_code == status.HTTP_201_CREATED
    tag = TagTour.objects.get(name="Минимальный тег")
    assert tag.description == "" or tag.description is None
    assert tag.tag_type == "" or tag.tag_type is None
