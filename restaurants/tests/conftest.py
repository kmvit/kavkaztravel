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

import random
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

# Фикстура для RestaurantType
@pytest.fixture
def restaurant_type(db):
    """Фикстура для типа ресторана."""
   
    return RestaurantType.objects.create(
        name="Кавказская кухня",
        description="Традиционные блюда народов Кавказа"
    )


# Фикстура для ресторана
@pytest.fixture
def restaurant(db, owner, child_region, restaurant_type, services):
    """Фикстура для ресторана со связанными объектами."""
   
    
    restaurant = Restaurant.objects.create(
        name="Ресторан 'Горный аул'",
        address="ул. Кавказская, 15",
        region=child_region,
        owner=owner,
        average_check=1500.00,
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

# Фикстура для родительского региона
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


# Фикстура для дочернего региона
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


# Фикстура для дополнительных регионов
@pytest.fixture
def additional_regions(db, parent_region, owner):
    """Фикстура для дополнительных регионов (например, города)."""
    return [
        Region.objects.create(
            name="Санкт-Петербург",
            url="spb",
            description="Культурная столица России",
            content="Информация о Санкт-Петербурге",
            seo_title="Санкт-Петербург - город",
            seo_description="Описание Санкт-Петербурга",
            parent=parent_region,
            owner=owner
        ),
        Region.objects.create(
            name="Новосибирск",
            url="novosibirsk",
            description="Научный центр Сибири",
            content="Информация о Новосибирске",
            seo_title="Новосибирск - город",
            seo_description="Описание Новосибирска",
            parent=parent_region,
            owner=owner
        )
    ]


# Фикстура для типа ресторана
@pytest.fixture
def restaurant_types(db):
    """Фикстура для типа ресторанов."""
    return [
        RestaurantType.objects.create(name="Кавказская кухня", description="Традиционные блюда народов Кавказа"),
        RestaurantType.objects.create(name="Японская кухня", description="Традиционные блюда японской кухни"),
        RestaurantType.objects.create(name="Итальянская кухня", description="Традиционные блюда Италии"),
        RestaurantType.objects.create(name="Фастфуд", description="Быстрая еда")
    ]


# Фикстура для услуг
@pytest.fixture
def services(db):
    """Фикстура для набора услуг."""
    return [
        Service.objects.create(name="Хаш"),
        Service.objects.create(name="Лобио"),
        Service.objects.create(name="Шашлык"),
        Service.objects.create(name="Суши"),
        Service.objects.create(name="Паста"),
        Service.objects.create(name="Пицца"),
        Service.objects.create(name="Барбекю"),
        Service.objects.create(name="Тортилья")
    ]


# Фикстура для ресторанов
@pytest.fixture
def restaurants(db, owner, child_region, additional_regions, restaurant_types, services):
    """Фикстура для создания 15 ресторанов с различными значениями."""
    restaurants = []
    for i in range(15):
        # Случайным образом выбираем тип ресторана
        r_type = random.choice(restaurant_types)
        # Случайным образом выбираем регион
        region = random.choice([child_region] + additional_regions)
        # Случайным образом выбираем услуги
        service_list = random.sample(services, random.randint(1, 3))  # Выбираем случайное количество услуг
        name = f"Ресторан {i+1} - {r_type.name}"
        address = f"ул. Адрес {i+1}, {region.name}"
        description = f"Описание ресторана {i+1} - {r_type.name}"
        working_hours = f"{random.randint(9, 11)}:00-{random.randint(19, 23)}:00"
        average_check = round(random.uniform(500, 3000), 2)

        # Создаем ресторан
        restaurant = Restaurant.objects.create(
            name=name,
            address=address,
            region=region,
            owner=owner,
            average_check=average_check,
            description=description,
            restaurant_type=r_type,
            working_hours=working_hours
        )

        restaurant.services.add(*service_list)

        # Добавляем изображение для ресторана
        image_file = SimpleUploadedFile(f"test_image_{i+1}.jpg", b"image_data", content_type="image/jpeg")
        RestaurantImage.objects.create(restaurant=restaurant, image=image_file)
        restaurants.append(restaurant)
    return restaurants
