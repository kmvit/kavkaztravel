import pytest
from rest_framework import status
from rest_framework.test import APIClient
from io import BytesIO
from PIL import Image
from kashiring.models import CarImage
from django.core.files.uploadedfile import InMemoryUploadedFile


@pytest.mark.django_db
def test_create_car_image(api_client, user, car_1):
    """Тестируем создание изображения для автомобиля"""
    api_client.force_authenticate(user=user)

    # Создаем изображение в памяти с помощью Pillow
    image = BytesIO()
    img = Image.new("RGB", (100, 100), color="red")
    img.save(image, "JPEG")
    image.seek(0)

    # Преобразуем в InMemoryUploadedFile для корректной отправки
    image_file = InMemoryUploadedFile(
        image, None, "image.jpg", "image/jpeg", image.tell(), None
    )

    # Отправляем запрос для создания изображения
    response = api_client.post(
        "/api/v1/kashiring/car-images/",
        {"car": car_1.id, "image": image_file},
        format="multipart",
    )

    # Проверяем, что ответ успешный и изображение создано
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.data
    assert response.data["car"] == car_1.id
    assert "image" in response.data


@pytest.mark.django_db
def test_list_car_images(api_client, user, car_1, car_1_images):
    """Тестируем получение списка изображений для автомобиля"""
    api_client.force_authenticate(user=user)

    # Отправляем GET запрос на получение списка изображений
    response = api_client.get("/api/v1/kashiring/car-images/")

    # Проверяем, что список изображений содержит хотя бы одно изображение для car_1
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == len(car_1_images)
    assert response.data[0]["car"] == car_1.id


@pytest.mark.django_db
def test_retrieve_car_image(api_client, user, car_1, car_1_images):
    """Тестируем получение одного изображения автомобиля"""
    api_client.force_authenticate(user=user)

    # Отправляем GET запрос для получения первого изображения по ID
    car_image = car_1_images[0]
    response = api_client.get(f"/api/v1/kashiring/car-images/{car_image.id}/")

    # Проверяем, что ответ содержит корректные данные
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == car_image.id
    assert response.data["car"] == car_1.id
    assert "image" in response.data


@pytest.mark.django_db
def test_delete_car_image(api_client, user, car_1, car_1_images):
    """Тестируем удаление изображения автомобиля"""
    api_client.force_authenticate(user=user)

    # Отправляем DELETE запрос для удаления изображения
    car_image = car_1_images[0]
    response = api_client.delete(f"/api/v1/kashiring/car-images/{car_image.id}/")

    # Проверяем, что изображение удалено
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert CarImage.objects.count() == len(car_1_images) - 1
