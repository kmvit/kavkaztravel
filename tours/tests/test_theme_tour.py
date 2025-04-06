import pytest
from rest_framework import status



# Вынесем адрес API в переменную
API_URL = "/api/v1/tours/themes/"


# Тестирование создания новой тематики тура через API
def test_create_theme_tour(api_client, user):
    """Тестирование создания новой тематики тура через API."""
    api_client.force_authenticate(user=user)
    data = {
        "name": "Приключенческий туризм",
        "description": "Туры с элементами приключений"
    }
    response = api_client.post(API_URL, data, format='json')
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "Приключенческий туризм"
    assert response.data["description"] == "Туры с элементами приключений"

# Тестирование чтения тематики тура через API
def test_read_theme_tour(api_client, theme_tour, user):
    """Тестирование чтения тематики тура через API."""
    response = api_client.get(f"{API_URL}{theme_tour.id}/", format='json')
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == theme_tour.name
    assert response.data["description"] == theme_tour.description

# Тестирование обновления тематики тура через API
def test_update_theme_tour(api_client, theme_tour, user):
    """Тестирование обновления тематики тура через API."""
    data = {
        "name": "Обновленный туризм",
        "description": "Новый описательный текст"
    }
    response = api_client.put(f"{API_URL}{theme_tour.id}/", data, format='json')
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Обновленный туризм"
    assert response.data["description"] == "Новый описательный текст"

# Тестирование удаления тематики тура через API
def test_delete_theme_tour(api_client, theme_tour, user):
    """Тестирование удаления тематики тура через API."""
    response = api_client.delete(f"{API_URL}{theme_tour.id}/", format='json')
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # Проверка, что объект действительно удален
    response_check = api_client.get(f"{API_URL}{theme_tour.id}/", format='json')
    assert response_check.status_code == status.HTTP_404_NOT_FOUND

# Тестирование уникальности имени тематики
def test_unique_theme_name(api_client, user):
    """Проверяем, что нельзя создать две тематики с одинаковым именем."""
    api_client.force_authenticate(user=user)
    data = {
        "name": "Экстремальный туризм",
        "description": "Для любителей адреналина"
    }
    
    # Первое создание - должно быть успешно
    response1 = api_client.post(API_URL, data, format='json')
    assert response1.status_code == status.HTTP_201_CREATED
    
    # Попытка создать дубликат
    response2 = api_client.post(API_URL, data, format='json')
    assert response2.status_code == status.HTTP_400_BAD_REQUEST
    assert 'name' in response2.data