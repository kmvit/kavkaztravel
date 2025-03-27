import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from restaurants.models import (
    RestaurantType,
    Service,
    Restaurant,
    RestaurantImage,
)
from datetime import datetime, timedelta

User = get_user_model()

from regions.models import Region
   
    

@pytest.fixture
def api_client():
    """Фикстура для API клиента."""
    return APIClient()


# Фикстура для владельца машины
@pytest.fixture
def owner(db):
    """Фикстура для пользователя-владельца."""
    User = get_user_model()
    return User.objects.create_user(
        username="owner_user", password="password123", email="owner@example.com"
    )


# Фикстура для арендатора (не владельца)
@pytest.fixture
def user(db):
    """Фикстура для пользователя, не являющегося владельцем рестораа."""
    User = get_user_model()
    return User.objects.create_user(
        username="renter_user", password="password123", email="renter@example.com"
    )

@pytest.fixture
def authenticated_api_client(owner):
    """Фикстура для аутентифицированного клиента API"""
    client = APIClient()
    client.force_authenticate(user=owner)  # Используем force_authenticate для DRF
    return client


@pytest.fixture
def parent_region(db, owner):
    """Фикстура для родительского региона (например, область)."""
    return Region.objects.create(
        name="Московская область",
        url="moskovskaya-oblast",
        description="Центральный регион России",
        content="Информация о Московской области",
        seo_title="Московская область - регион",
        seo_description="Описание Московской области",
        owner=owner
    )

@pytest.fixture
def child_region(db, parent_region, owner):
    """Фикстура для дочернего региона (например, город)."""
    return Region.objects.create(
        name="Москва",
        url="moscow",
        description="Столица России",
        content="Информация о Москве",
        seo_title="Москва - столица",
        seo_description="Описание Москвы",
        parent=parent_region,
        owner=owner
    )

# Фикстура для RestaurantType
@pytest.fixture
def restaurant_type(db):
    """Фикстура для типа ресторана."""
   
    return RestaurantType.objects.create(
        name="Кавказская кухня",
        description="Традиционные блюда народов Кавказа"
    )

# Фикстура для Service
@pytest.fixture
def services(db):
    """Фикстура для набора услуг."""
    return [
        Service.objects.create(name="Хаш"),
        Service.objects.create(name="Лобио"),
        Service.objects.create(name="Шашлык")
    ]

# Фикстура для ресторана
@pytest.fixture
def restaurant(db, owner, region, restaurant_type, services):
    """Фикстура для ресторана со связанными объектами."""
   
    
    restaurant = Restaurant.objects.create(
        name="Ресторан 'Горный аул'",
        address="ул. Кавказская, 15",
        region=child_region,
        owner=owner,
        average_check=Decimal("1500.00"),
        description="Лучшие блюда кавказской кухни",
        restaurant_type=restaurant_type,
        working_hours="10:00-22:00"
    )
    
    # Добавляем M2M связи
    restaurant.services.add(*services)
    return restaurant


from django.core.files.uploadedfile import SimpleUploadedFile



@pytest.fixture
def restaurant_image_1(restaurant):
    image_file = SimpleUploadedFile("test_image_1.jpg", b"image_data", content_type="image/jpeg")
    return RestaurantImage.objects.create(restaurant=restaurant, image=image_file)

@pytest.fixture
def restaurant_image_2(restaurant):
    image_file = SimpleUploadedFile("test_image_2.jpg", b"image_data", content_type="image/jpeg")
    return RestaurantImage.objects.create(restaurant=restaurant, image=image_file)

@pytest.fixture
def restaurant_image_3(restaurant):
    image_file = SimpleUploadedFile("test_image_3.jpg", b"image_data", content_type="image/jpeg")
    return RestaurantImage.objects.create(restaurant=restaurant, image=image_file)

@pytest.fixture
def restaurant_image_4(restaurant):
    image_file = SimpleUploadedFile("test_image_4.jpg", b"image_data", content_type="image/jpeg")
    return RestaurantImage.objects.create(restaurant=restaurant, image=image_file)

@pytest.fixture
def restaurant_image_5(restaurant):
    image_file = SimpleUploadedFile("test_image_5.jpg", b"image_data", content_type="image/jpeg")
    return RestaurantImage.objects.create(restaurant=restaurant, image=image_file)


