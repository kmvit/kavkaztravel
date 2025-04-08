import pytest
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
URL = '/api/v1/tours/gallery_tour/'

@pytest.mark.django_db
def test_create_valid(api_client, tour, image_file):
    """Успешное создание элемента галереи"""
    response = api_client.post(
        URL,
        {'tour': tour.id, 'image': image_file},
        format='multipart'
    )
    
    print("\n=== DEBUG INFORMATION ===")
    print(f"File size: {len(image_file.read())} bytes")
    image_file.seek(0)  # Возвращаем указатель в начало файла
    print(f"File content start: {image_file.read(10)}")
    image_file.seek(0)
    print(f"Response data: {response.data}")
    
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_retrieve_item(api_client, gallery_item):
    """Получение конкретного элемента"""
    response = api_client.get(f"{URL}{gallery_item.id}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == gallery_item.id

@pytest.mark.django_db
def test_list_items(api_client, gallery_item):
    """Получение списка элементов"""
    response = api_client.get(URL)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1

import pytest
from rest_framework import status



@pytest.mark.django_db
def test_update_item(api_client, gallery_item, image_file):
    """Обновление изображения"""
    from PIL import Image
    import io
    
    # Создаем минимальное валидное изображение 1x1 пиксель
    image = Image.new('RGB', (1, 1), color='red')
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    
    return SimpleUploadedFile(
        name='test_image.jpg',
        content=img_byte_arr.getvalue(),
        content_type='image/jpeg'
    )
    response = api_client.patch(
        f"{URL}{gallery_item.id}/",
        {'image': new_file},
        format='multipart'
    )
    assert response.status_code == status.HTTP_200_OK
    assert 'new_image' in response.data['image']


import pytest
from rest_framework import status

URL = '/api/v1/tours/gallery_tour/'

@pytest.mark.django_db
def test_delete_item(api_client, gallery_item):
    """Удаление элемента галереи"""
    response = api_client.delete(f"{URL}{gallery_item.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = api_client.get(f"{URL}{gallery_item.id}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND

import pytest
from rest_framework import status

TOUR_URL = '/api/v1/tours/'
GALLERY_URL = '/api/v1/tours/gallery_tour/'

@pytest.mark.django_db
def test_tour_has_gallery(api_client, tour, gallery_item):
    """Проверка связи тур-галерея"""
    response = api_client.get(f"{TOUR_URL}{tour.id}/")
    assert response.status_code == status.HTTP_200_OK
    assert any(img['id'] == gallery_item.id for img in response.data['gallery_tour'])