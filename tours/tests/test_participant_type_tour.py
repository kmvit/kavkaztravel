import pytest
from rest_framework import status
from tours.models import ParticipantTypeTour
    
    

API_URL = "/api/v1/tours/participant_types/"

# CRUD Tests
def test_create_participant_type(api_client, user):
    """Тестирование создания типа участников."""
    data = {
        "name": "Взрослые",
        "description": "Туры для взрослых участников"
    }
    response = api_client.post(API_URL, data, format='json')
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == data["name"]
    assert response.data["description"] == data["description"]

def test_read_participant_type(api_client, participant_type_tour):
    """Тестирование чтения типа участников."""
    response = api_client.get(f"{API_URL}{participant_type_tour.id}/")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == participant_type_tour.name
    assert response.data["description"] == participant_type_tour.description

def test_update_participant_type(api_client, participant_type_tour, user):
    """Тестирование полного обновления типа участников."""
    api_client.force_authenticate(user=user)
    data = {
        "name": "Обновленный тип",
        "description": "Новое описание типа"
    }
    response = api_client.put(
        f"{API_URL}{participant_type_tour.id}/", 
        data, 
        format='json'
    )
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == data["name"]
    assert response.data["description"] == data["description"]

def test_delete_participant_type(api_client, participant_type_tour, user):
    """Тестирование удаления типа участников."""
    api_client.force_authenticate(user=user)
    response = api_client.delete(f"{API_URL}{participant_type_tour.id}/")
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response_check = api_client.get(f"{API_URL}{participant_type_tour.id}/")
    assert response_check.status_code == status.HTTP_404_NOT_FOUND

# Дополнительные тесты
def test_unique_participant_type_name(api_client, user):
    """Тестирование уникальности имени типа участников."""
    api_client.force_authenticate(user=user)
    data = {
        "name": "Корпоративные группы",
        "description": "Для организаций"
    }
    
    # Первое создание
    response1 = api_client.post(API_URL, data, format='json')
    assert response1.status_code == status.HTTP_201_CREATED
    
    # Попытка дублирования
    response2 = api_client.post(API_URL, data, format='json')
    assert response2.status_code == status.HTTP_400_BAD_REQUEST
    assert 'name' in response2.data

def test_participant_type_validation(api_client, user):
    """Тестирование валидации данных типа участников."""
    api_client.force_authenticate(user=user)
    
    # Случай 1: Отсутствует обязательное поле name
    invalid_data = {"description": "Описание без имени"}
    response = api_client.post(API_URL, invalid_data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'name' in response.data


def test_participant_type_list(api_client, user, participant_type_tour):
    """Тестирование получения списка типов участников."""
    api_client.force_authenticate(user=user)
    
    # Создаем дополнительные типы через фабрику
    ParticipantTypeTour.objects.create(name="Пенсионеры")
    ParticipantTypeTour.objects.create(name="Студенты")
    
    response = api_client.get(API_URL)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) >= 3  # Проверяем что есть как минимум 3 элемента
    assert any(item['name'] == "Семьи с детьми" for item in response.data)