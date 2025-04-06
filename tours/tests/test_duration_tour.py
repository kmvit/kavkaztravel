import pytest
from rest_framework import status
from tours.models import DurationTour

API_URL = "/api/v1/tours/durations/"

# CRUD Tests
def test_create_duration_tour(api_client, user):
    """Тестирование создания продолжительности тура."""
    data = {"name": "2 часа"}
    response = api_client.post(API_URL, data, format='json')
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == data["name"]

def test_read_duration_tour(api_client, duration_tour):
    """Тестирование чтения продолжительности тура."""
    response = api_client.get(f"{API_URL}{duration_tour.id}/")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == duration_tour.name

def test_update_duration_tour(api_client, duration_tour, user):
    """Тестирование полного обновления продолжительности тура."""
    data = {"name": "3 дня"}
    response = api_client.put(
        f"{API_URL}{duration_tour.id}/", 
        data, 
        format='json'
    )
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == data["name"]

def test_delete_duration_tour(api_client, duration_tour, user):
    """Тестирование удаления продолжительности тура."""
    api_client.force_authenticate(user=user)
    response = api_client.delete(f"{API_URL}{duration_tour.id}/")
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response_check = api_client.get(f"{API_URL}{duration_tour.id}/")
    assert response_check.status_code == status.HTTP_404_NOT_FOUND

# Additional Tests
def test_unique_duration_name(api_client, user):
    """Тестирование уникальности названия продолжительности."""
    api_client.force_authenticate(user=user)
    data = {"name": "1 неделя"}
    
    # Первое создание
    response1 = api_client.post(API_URL, data, format='json')
    assert response1.status_code == status.HTTP_201_CREATED
    
    # Попытка дублирования
    response2 = api_client.post(API_URL, data, format='json')
    assert response2.status_code == status.HTTP_400_BAD_REQUEST
    assert 'name' in response2.data

def test_duration_validation(api_client, user):
    """Тестирование валидации данных продолжительности."""
    api_client.force_authenticate(user=user)
    
    # Случай 1: Отсутствует обязательное поле name
    response = api_client.post(API_URL, {}, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'name' in response.data
 
def test_duration_list(api_client, duration_tour):
    """Тестирование получения списка продолжительностей."""
    # Создаем дополнительные продолжительности
    DurationTour.objects.create(name="1 день")
    DurationTour.objects.create(name="2 недели")
    
    response = api_client.get(API_URL)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) >= 3  # Проверяем что есть как минимум 3 элемента
    assert any(item['name'] == "5 дней" for item in response.data)

def test_duration_empty_name(api_client, user):
    """Тестирование создания с пустым названием."""
    api_client.force_authenticate(user=user)
    response = api_client.post(API_URL, {"name": ""}, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'name' in response.data

def test_duration_whitespace_name(api_client, user):
    """Тестирование создания с названием из пробелов."""
    response = api_client.post(API_URL, {"name": "   "}, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'name' in response.data
