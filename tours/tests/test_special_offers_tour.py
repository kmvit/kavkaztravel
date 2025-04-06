import pytest
from rest_framework import status
from tours.models import SpecialOfferTour

API_URL = "/api/v1/tours/special_offers/"

# CRUD Tests
def test_create_special_offer(api_client, user):
    """Тестирование создания спецпредложения."""
    data = {
        "offer_type": "Раннее бронирование",
        "description": "Скидка 20% при бронировании за 3 месяца"
    }
    response = api_client.post(API_URL, data, format='json')
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["offer_type"] == data["offer_type"]
    assert response.data["description"] == data["description"]

def test_read_special_offer(api_client, special_offer_tour):
    """Тестирование чтения спецпредложения."""
    response = api_client.get(f"{API_URL}{special_offer_tour.id}/")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data["offer_type"] == special_offer_tour.offer_type
    assert response.data["description"] == special_offer_tour.description

def test_update_special_offer(api_client, special_offer_tour, user):
    """Тестирование полного обновления спецпредложения."""
    api_client.force_authenticate(user=user)
    data = {
        "offer_type": "Новогодняя акция",
        "description": "Специальные условия на праздники"
    }
    response = api_client.put(
        f"{API_URL}{special_offer_tour.id}/", 
        data, 
        format='json'
    )
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data["offer_type"] == data["offer_type"]
    assert response.data["description"] == data["description"]

def test_delete_special_offer(api_client, special_offer_tour, user):
    """Тестирование удаления спецпредложения."""
    api_client.force_authenticate(user=user)
    response = api_client.delete(f"{API_URL}{special_offer_tour.id}/")
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response_check = api_client.get(f"{API_URL}{special_offer_tour.id}/")
    assert response_check.status_code == status.HTTP_404_NOT_FOUND

# Additional Tests
def test_special_offer_validation(api_client, user):
    """Тестирование валидации данных спецпредложения."""
  
    # Случай 1: Отсутствует обязательное поле offer_type
    response = api_client.post(API_URL, {"description": "Без типа"}, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'offer_type' in response.data
    


def test_special_offer_list(api_client, special_offer_tour):
    """Тестирование получения списка спецпредложений."""
    # Создаем дополнительные предложения
    SpecialOfferTour.objects.create(offer_type="Черная пятница")
    SpecialOfferTour.objects.create(offer_type="Летний сезон")
    
    response = api_client.get(API_URL)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) >= 3  # Проверяем что есть как минимум 3 элемента
    assert any(item['offer_type'] == "Скидка 15%" for item in response.data)

def test_empty_description(api_client, user):
    """Тестирование создания с пустым описанием."""
    api_client.force_authenticate(user=user)
    data = {"offer_type": "Акция", "description": ""}
    response = api_client.post(API_URL, data, format='json')
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["description"] == ""

def test_null_description(api_client, user):
    """Тестирование создания с null-описанием."""
    api_client.force_authenticate(user=user)
    data = {"offer_type": "Акция", "description": None}
    response = api_client.post(API_URL, data, format='json')
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["description"] is None

def test_partial_update(api_client, special_offer_tour, user):
    """Тестирование частичного обновления."""
    api_client.force_authenticate(user=user)
    update_data = {"description": "Обновленные условия"}
    
    response = api_client.patch(
        f"{API_URL}{special_offer_tour.id}/", 
        update_data, 
        format='json'
    )
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data["description"] == update_data["description"]
    assert response.data["offer_type"] == special_offer_tour.offer_type