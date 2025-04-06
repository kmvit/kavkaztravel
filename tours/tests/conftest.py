import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from regions.models import Region
from tours.models import (
    TourOperator, Tour, AttractionTour, ThemeTour, ParticipantTypeTour,
    FormatTour, DurationTour, SpecialOfferTour, GalleryTour,
    AvailableDateTour, Order
)

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



import pytest
from datetime import date, timedelta

# Фикстуры для моделей туров
@pytest.fixture
def tour_operator(db, owner, parent_region):
    """
    Фикстура для создания тестового туроператора. 
    """
    return TourOperator.objects.create(
        region=parent_region,
        owner=owner,
        license_number="TO-123456"
    )

@pytest.fixture
def theme_tour(db):
    """
    Фикстура для создания тестовой тематики тура.
    """
    return ThemeTour.objects.create(
        name="Экстремальный туризм",
        description="Туры с элементами экстрима"
    )

@pytest.fixture
def attraction_tour(db, parent_region):
    """
    Фикстура для создания тестовой достопримечательности.
    """
    return AttractionTour.objects.create(
        name="Эльбрус",
        description="Высочайшая вершина России",
        region=parent_region
    )

@pytest.fixture
def participant_type_tour(db):
    """Фикстура для типа участников тура."""
    return ParticipantTypeTour.objects.create(
        name="Семьи с детьми",
        description="Тур для семейного отдыха"
    )

@pytest.fixture
def format_tour(db):
    """Фикстура для формата проведения тура."""
    return FormatTour.objects.create(
        name="Индивидуальный",
        description="Персональный тур"
    )

@pytest.fixture
def duration_tour(db):
    """Фикстура описывающая продолжительность тура."""
    return DurationTour.objects.create(name="5 дней")

@pytest.fixture
def special_offer_tour(db):
    """Фикстура для спецпредложений или скидки для тура."""
    return SpecialOfferTour.objects.create(
        offer_type="Скидка 15%",
        description="Сезонное предложение"
    )

@pytest.fixture
def tour(db, owner, parent_region, theme_tour, duration_tour, 
        special_offer_tour, attraction_tour, participant_type_tour, 
        format_tour):
    """Фикстура для тура."""        
    tour = Tour.objects.create(
        guide=owner,
        title="Экскурсия по Москве",
        description="Обзорная экскурсия по столице",
        terms="Без ограничений",
        region=parent_region,
        price=5000.00,
        theme=theme_tour,
        duration=duration_tour,
        special_offer=special_offer_tour
    )
    
    # Добавляем M2M связи
    tour.attractions.add(attraction_tour)
    tour.participant_types.add(participant_type_tour)
    tour.formats.add(format_tour)
    
    return tour

@pytest.fixture
def gallery_tour(db, tour):
    return GalleryTour.objects.create(tour=tour)

@pytest.fixture
def available_date_tour(db, tour):
    return AvailableDateTour.objects.create(
        tour=tour,
        start_date=date.today() + timedelta(days=7),
        end_date=date.today() + timedelta(days=10),
        is_active=True
    )

@pytest.fixture
def order(db, tour, user):
    return Order.objects.create(
        tour=tour,
        date=date.today() + timedelta(days=14),
        size=2,
        username="test_client",
        email="client@test.ru",
        phone="+79001234567",
        owner=user
    )