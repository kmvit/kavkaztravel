import pytest
from rest_framework import status
from tours.models import FormatTour

API_URL = "/api/v1/tours/formats/"

# CRUD Tests
def test_create_format_tour(api_client, user):
    """Тестирование создания формата тура."""
    data = {
        "name": "Групповой",
        "description": "Тур для группы участников"
    }
    response = api_client.post(API_URL, data, format='json')
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == data["name"]
    assert response.data["description"] == data["description"]

def test_read_format_tour(api_client, format_tour):
    """Тестирование чтения формата тура."""
    response = api_client.get(f"{API_URL}{format_tour.id}/")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == format_tour.name
    assert response.data["description"] == format_tour.description

def test_update_format_tour(api_client, format_tour, user):
    """Тестирование полного обновления формата тура."""
    api_client.force_authenticate(user=user)
    data = {
        "name": "Обновленный формат",
        "description": "Новое описание формата"
    }
    response = api_client.put(
        f"{API_URL}{format_tour.id}/", 
        data, 
        format='json'
    )
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == data["name"]
    assert response.data["description"] == data["description"]

def test_delete_format_tour(api_client, format_tour, user):
    """Тестирование удаления формата тура."""
    response = api_client.delete(f"{API_URL}{format_tour.id}/")
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response_check = api_client.get(f"{API_URL}{format_tour.id}/")
    assert response_check.status_code == status.HTTP_404_NOT_FOUND

def test_unique_format_tour_name(api_client, user):
    """Тестирование уникальности имени формата тура."""
    api_client.force_authenticate(user=user)
    data = {
        "name": "Онлайн",
        "description": "Виртуальный тур"
    }
    
    # Первое создание
    response1 = api_client.post(API_URL, data, format='json')
    assert response1.status_code == status.HTTP_201_CREATED
    
    # Попытка дублирования
    response2 = api_client.post(API_URL, data, format='json')
    assert response2.status_code == status.HTTP_400_BAD_REQUEST
    assert 'name' in response2.data

def test_format_tour_validation(api_client, user):
    """Тестирование валидации данных формата тура."""
    api_client.force_authenticate(user=user)
    
    # Случай 1: Отсутствует обязательное поле name
    invalid_data = {"description": "Описание без имени"}
    response = api_client.post(API_URL, invalid_data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'name' in response.data
    

def test_partial_update_format_tour(api_client, format_tour, user):
    """Тестирование частичного обновления формата тура."""
    api_client.force_authenticate(user=user)
    update_data = {"description": "Обновленное описание формата"}
    
    response = api_client.patch(
        f"{API_URL}{format_tour.id}/", 
        update_data, 
        format='json'
    )
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data["description"] == update_data["description"]
    assert response.data["name"] == format_tour.name

def test_format_tour_list(api_client, user, format_tour):
    """Тестирование получения списка форматов туров."""
    api_client.force_authenticate(user=user)
    
    # Создаем дополнительные форматы
    FormatTour.objects.create(name="Гибридный")
    FormatTour.objects.create(name="Корпоративный")
    
    response = api_client.get(API_URL)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) >= 3  # Проверяем что есть как минимум 3 элемента
    assert any(item['name'] == "Индивидуальный" for item in response.data)


def test_format_tour_empty_description(api_client, user):
    """Тестирование создания формата с пустым описанием."""
    api_client.force_authenticate(user=user)
    data = {
        "name": "Автобусный",
        "description": ""
    }
    response = api_client.post(API_URL, data, format='json')
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["description"] == ""