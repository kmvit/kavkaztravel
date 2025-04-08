import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from regions.models import Region
from tours.models import TourOperator, Tour, TagTour, AvailableDateTour, Order, GalleryTour
from core.models import BaseContent
from django.core.files.uploadedfile import SimpleUploadedFile
User = get_user_model()




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
    """Фикстура для пользователя, не являющегося владельцем машины."""
    User = get_user_model()
    return User.objects.create_user(
        username="renter_user", password="password123", email="renter@example.com"
    )

@pytest.fixture
def api_client(user):
    """Фикстура для клиента API с авторизованным пользователем."""
    client = APIClient()
    client.force_authenticate(user=user)
    return client

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
        owner=owner,
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
        owner=owner,
    )



from core.models import BaseContent





@pytest.fixture
def region(db):
    """Создание региона."""
    return Region.objects.create(
        name='Московская область'
    )


@pytest.fixture
def tour_operator(db, region, user):
    """Создание туроператора."""
    return TourOperator.objects.create(
        region=region,
        owner=user,
        license_number="1234567890"
    )


@pytest.fixture
def tag(db):
    """Создание тега для тура."""
    return TagTour.objects.create(
        name='Пешеходный',
        description='Тур для любителей пеших прогулок',
        tag_type='Тип 1'
    )


@pytest.fixture
def tour(db, region, user, tag):
    """Создание тура."""
    tour = Tour.objects.create(
        guide=user,
        title="Горный тур в Алтай",
        description="Тур по горам Алтая",
        terms="Условия туров",
        region=region,
        price=12000.00,
    )
    tour.tags.add(tag)
    return tour


@pytest.fixture
def available_date_tour(db, tour):
    """Создание доступной даты для тура."""
    return AvailableDateTour.objects.create(
        tour=tour,
        start_date="2025-05-01",
        end_date="2025-05-10",
        is_active=True
    )


@pytest.fixture
def order(db, tour, user):
    """Создание заказа для тура."""
    return Order.objects.create(
        tour=tour,
        date="2025-05-05",
        size=2,
        username="client_name",
        email="client@example.com",
        phone="+71234567890",
        owner=user
    )

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.fixture
def valid_image():
    """Создает валидное тестовое изображение"""
    return SimpleUploadedFile(
        name='test_image.jpg',
        content=b'\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xFF\xDB\x00',  # Минимальный валидный JPEG
        content_type='image/jpeg'
    )

@pytest.fixture
def gallery_data(tour, valid_image):
    """Данные для создания элемента галереи"""
    return {
        'tour': tour.id,
        'image': valid_image
    }