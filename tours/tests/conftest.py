import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from regions.models import Region
from tours.models import (
    TourOperator,
    Tour,
    TagTour,
    AvailableDateTour,
    Order,
    GalleryTour,
)
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
def api_client(owner):
    """Фикстура для клиента API с авторизованным пользователем."""
    client = APIClient()
    client.force_authenticate(user=owner)
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
def tour_operator(db, child_region, owner):
    """Фикстура для существующего туроператора."""
    return TourOperator.objects.create(
        region=child_region,
        owner=owner,
        license_number="TO-654321",
        name="Существующий туроператор",
        url="existing-tour-operator",
        description="Описание существующего",
        content="Контент существующего",
        seo_title="SEO существующего",
        seo_description="SEO описание существующего",
    )


@pytest.fixture
def region(db):
    """Создание региона."""
    return Region.objects.create(name="Московская область")


@pytest.fixture
def tour_operator(db, region, owner):
    """Создание туроператора."""
    return TourOperator.objects.create(
        region=region, owner=owner, license_number="1234567890"
    )


@pytest.fixture
def tag(db):
    """Создание тега для тура."""
    return TagTour.objects.create(
        name="Пешеходный",
        description="Тур для любителей пеших прогулок",
        tag_type="Тип 1",
    )


@pytest.fixture
def tour(db, region, owner, tag):
    """Создание тура."""
    tour = Tour.objects.create(
        guide=owner,
        title="Горный тур в Алтай",
        description="Тур по горам Алтая",
        terms="Условия туров",
        region=region,
        price=12000.00,
    )
    tour.tags.add(tag)
    return tour


@pytest.fixture
def tags(db):
    """Создание нескольких тегов для туров."""
    tag1 = TagTour.objects.create(
        name="Пешеходный",
        description="Тур для любителей пеших прогулок",
        tag_type="Тип 1",
    )
    tag2 = TagTour.objects.create(
        name="Горный", description="Тур по горам Алтая", tag_type="Тип 2"
    )
    tag3 = TagTour.objects.create(
        name="Летний", description="Летний тур по Алтаю", tag_type="Тип 3"
    )
    tag4 = TagTour.objects.create(
        name="Культурный", description="Тур по историческим местам", tag_type="Тип 4"
    )
    return [tag1, tag2, tag3, tag4]


@pytest.fixture
def tours(db, owner, region, tags):
    """Создание нескольких туров с разными тегами."""
    tours = [
        Tour.objects.create(
            guide=owner,
            title="Горный тур в Алтай",
            description="Тур по горам Алтая",
            region=region,
            price=12000.00,
        ),
        Tour.objects.create(
            guide=owner,
            title="Пешеходный тур",
            description="Тур для любителей пеших прогулок",
            region=region,
            price=8000.00,
        ),
        Tour.objects.create(
            guide=owner,
            title="Летний тур",
            description="Летний тур по Алтаю",
            region=region,
            price=10000.00,
        ),
        Tour.objects.create(
            guide=owner,
            title="Культурный тур",
            description="Тур по историческим местам",
            region=region,
            price=9000.00,
        ),
    ]

    # Присваиваем теги разным турам
    tours[0].tags.add(tags[1], tags[0])  # Горный и Пешеходный
    tours[1].tags.add(tags[0])  # Пешеходный
    tours[2].tags.add(tags[2])  # Летний
    tours[3].tags.add(tags[3])  # Культурный
    return tours


@pytest.fixture
def available_date_tour(db, tour):
    """Создание доступной даты для тура."""
    return AvailableDateTour.objects.create(
        tour=tour, start_date="2025-05-01", end_date="2025-05-10", is_active=True
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
        owner=user,
    )


@pytest.fixture
def image_file():
    """Создает действительно валидное тестовое изображение"""
    from PIL import Image
    import io

    # Создаем минимальное валидное изображение 1x1 пиксель
    image = Image.new("RGB", (1, 1), color="red")
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="JPEG")

    return SimpleUploadedFile(
        name="test_image.jpg",
        content=img_byte_arr.getvalue(),
        content_type="image/jpeg",
    )


@pytest.fixture
def gallery_item(tour, image_file):
    """Фикстура для элемента галереи"""
    return GalleryTour.objects.create(tour=tour, image=image_file)
