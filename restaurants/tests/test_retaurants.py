import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from restaurants.models import Restaurant, RestaurantImage
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_create_restaurant(authenticated_api_client, child_region, services):
    """Тест создания ресторана"""
    # Подготовка данных
    data = {
        "name": "New Restaurant",
        "address": "Test Address",
        "region": child_region.id,  
        "average_check": "2000.00",  # Корректный формат для Decimal
        "description": "Test Description",
        "working_hours": "10:00-22:00",
        "restaurant_type": {  # Обязательное поле
            "name": "Test Type",
            "description": "Type Description"
        },
        "services": [  # Обязательное поле
            {
                "name": "789",  # Используем существующую услугу
                "description": "wi-fi"
            }
        ]
    }

    # Отправка запроса
    response = authenticated_api_client.post("/api/v1/restaurants/meal/", data, format='json')
    
    # Проверки
    assert response.status_code == 201, response.data
    assert response.data["name"] == "New Restaurant"

@pytest.mark.django_db
def test_list_restaurants(api_client, restaurant):
    """Тест получения списка ресторанов"""
    response = api_client.get("/restaurants/")
    assert response.status_code == 200
    assert len(response.data) > 0

@pytest.mark.django_db
def test_get_restaurant_detail(api_client, restaurant):
    """Тест получения информации о конкретном ресторане"""
    response = api_client.get(f"/restaurants/{restaurant.id}/")
    assert response.status_code == 200
    assert response.data["name"] == restaurant.name

@pytest.mark.django_db
def test_update_restaurant(authenticated_api_client, restaurant):
    """Тест частичного обновления ресторана"""
    response = authenticated_api_client.patch(f"/restaurants/{restaurant.id}/", {"name": "Updated Name"})
    assert response.status_code == 200
    assert response.data["name"] == "Updated Name"

@pytest.mark.django_db
def test_delete_restaurant(authenticated_api_client, restaurant):
    """Тест удаления ресторана"""
    response = authenticated_api_client.delete(f"/restaurants/{restaurant.id}/")
    assert response.status_code == 204
    assert not Restaurant.objects.filter(id=restaurant.id).exists()

# === Тесты с изображениями === #

@pytest.mark.django_db
def test_create_restaurant_with_images(authenticated_api_client):
    """Тест создания ресторана с изображениями"""
    image_file = SimpleUploadedFile("test_image.jpg", b"image_data", content_type="image/jpeg")
    
    response = authenticated_api_client.post(
        "/restaurants/", 
        {
            "name": "New Restaurant",
            "address": "Test Address",
            "average_check": 2000,
            "description": "Test Description",
            "working_hours": "10:00-22:00",
            "images": [image_file]
        },
        format="multipart"
    )
    
    assert response.status_code == 201
    assert "images" in response.data
    assert len(response.data["images"]) > 0

@pytest.mark.django_db
def test_get_restaurant_with_images(api_client, restaurant, multiple_restaurant_images):
    """Тест получения ресторана с изображениями"""
    response = api_client.get(f"/restaurants/{restaurant.id}/")
    
    assert response.status_code == 200
    assert "images" in response.data
    assert len(response.data["images"]) == 3

@pytest.mark.django_db
def test_update_restaurant_with_new_image(authenticated_api_client, restaurant):
    """Тест обновления ресторана с добавлением нового изображения"""
    new_image = SimpleUploadedFile("new_image.jpg", b"new_image_data", content_type="image/jpeg")
    
    response = authenticated_api_client.patch(
        f"/restaurants/{restaurant.id}/", 
        {"images": [new_image]}, 
        format="multipart"
    )

    assert response.status_code == 200
    assert len(response.data["images"]) > 0

@pytest.mark.django_db
def test_delete_restaurant_image(authenticated_api_client, restaurant_image_1):
    """Тест удаления изображения ресторана"""
    image_id = restaurant_image_1.id
    response = authenticated_api_client.delete(f"/restaurant-images/{image_id}/")
    
    assert response.status_code == 204
    assert not RestaurantImage.objects.filter(id=image_id).exists()
'''