import pytest
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
URL = '/api/v1/tours/gallery_tour/'

import pytest
from rest_framework import status

URL = '/api/v1/tours/gallery_tour/'

@pytest.mark.django_db
def test_create_gallery_item(api_client, gallery_data):
    """Успешное создание элемента галереи"""
    response = api_client.post(
        URL,
        data=gallery_data,
        format='multipart'
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    assert 'id' in response.data
    assert 'image' in response.data
    assert response.data['tour'] == gallery_data['tour']

@pytest.mark.django_db
def test_create_without_image(api_client, tour):
    """Попытка создания без изображения"""
    response = api_client.post(
        URL,
        data={'tour': tour.id},
        format='multipart'
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'image' in response.data

import pytest
from rest_framework import status



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
    new_file = SimpleUploadedFile(
        name='new_image.jpg',
        content=b'\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x00',  # другой минимальный JPEG
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