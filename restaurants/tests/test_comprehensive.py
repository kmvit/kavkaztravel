import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from restaurants.models import Restaurant, RestaurantImage, Service, RestaurantType
from django.contrib.auth import get_user_model
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import transaction, IntegrityError
from rest_framework import status
from django.db.models import Q

User = get_user_model()

BASE_ULR = "/api/v1/restaurants/meal/"


@pytest.mark.django_db
def test_filter_restaurants(
    api_client, restaurants, authenticated_api_client, child_region
):
    """
    Комплексный тест:
    1. Проверяет начальное состояние
    2. Создает новые рестораны с типом и услугой
    3. Проверяет увеличение счетчиков в моделях
    4. Тестирует фильтрацию через API
    5. Сравнивает результаты API с прямым запросом к модели
    6. Проверяет конечное состояние всех моделей
    """
    from restaurants.models import Restaurant, RestaurantType, Service
    import json

    # 1. Проверка начального состояния
    initial_counts = {
        "restaurants": Restaurant.objects.count(),
        "types": RestaurantType.objects.count(),
        "services": Service.objects.count(),
        "images": RestaurantImage.objects.count(),
    }

    # 2. Создание нового ресторана
    for i in range(10):
        new_restaurant_data = {
            "name": "Ресторан 'Сказка'",
            "address": "ул. Волшебная, 10",
            "region": child_region.id,
            "average_check": 1800.00,
            "description": "Авторская кухня с элементами восточной гастрономии",
            "working_hours": "12:00-23:00",
            "restaurant_type": {
                "name": "Итальянская кухня",
                "description": "Традиционные блюда Италии",
            },
            "services": [{"name": "Пицца", "description": "Курьерская доставка еды"}],
        }

        # 3. Отправка запроса и проверка создания
        response_create = authenticated_api_client.post(
            BASE_ULR,
            data=json.dumps(new_restaurant_data),
            content_type="application/json",
        )
        assert (
            response_create.status_code == 201
        ), f"Ошибка создания: {response_create.status_code}, {response_create.data}"
        new_restaurant_id = response_create.data["id"]
    # 4. Проверка изменений в БД
    after_creation_counts = {
        "restaurants": Restaurant.objects.count(),
        "types": RestaurantType.objects.count(),
        "services": Service.objects.count(),
    }

    assert after_creation_counts["restaurants"] == 25
    assert after_creation_counts["types"] == 3
    assert after_creation_counts["services"] == 8


    # Формируем строку запроса с параметрами
    filter_url = f"/api/v1/restaurants/meal/?region={child_region}&average_check_min=1000&average_check_max=2000"

    # Выполняем GET-запрос с параметрами
    response_filter = api_client.get(filter_url)

    # Проверка, что API отработало корректно
    assert (
        response_filter.status_code == 200
    ), f"Ошибка фильтрации: {response_filter.status_code}, {response_filter.data}"

    # Выводим результат ответа от API
    print("API response:", response_filter.data)

    # Извлекаем ID ресторанов из ответа API
    api_restaurants = response_filter.data["results"]
    api_ids = {
        r["id"] for r in api_restaurants
    }  # Создаем набор ID ресторанов из API ответа

    from django.db.models import Q

    db_restaurants = Restaurant.objects.filter(
        Q(region__name__icontains=child_region)
        & Q(average_check__gte=1000)
        & Q(average_check__lte=2000)
    )
    db_ids = set(
        db_restaurants.values_list("id", flat=True)
    )  # Набор ID ресторанов из базы данных
    print("Database IDs:", db_ids)

    # Основная проверка соответствия
    assert (
        api_ids == db_ids
    ), f"Расхождение: API вернуло {api_ids}, модель содержит {db_ids}"

    # 3. Извлекаем первый ресторан из результатов API
    api_restaurant = response_filter.data["results"][0]
    api_restaurant_id = api_restaurant["id"]

    # 4. Выполняем запрос через API для получения информации о ресторане по ID
    api_restaurant_detail_url = f"/api/v1/restaurants/meal/{api_restaurant_id}/"
    response_api_detail = api_client.get(api_restaurant_detail_url)

    # Проверка, что API отработало корректно
    assert (
        response_api_detail.status_code == 200
    ), f"Ошибка запроса детальной информации для ресторана: {response_api_detail.status_code}, {response_api_detail.data}"

    # 5. Прямой запрос к базе данных для получения того же ресторана
    from django.db.models import Q

    db_restaurant = Restaurant.objects.get(id=api_restaurant_id)

    # 6. Сравниваем данные
    # Сравниваем имя ресторана
    assert (
        response_api_detail.data["name"] == db_restaurant.name
    ), f"Несоответствие имени ресторана: {response_api_detail.data['name']} != {db_restaurant.name}"

    # Сравниваем регион ресторана
    assert (
        response_api_detail.data["region"] == db_restaurant.region.id
    ), f"Несоответствие региона для ресторана с ID {api_restaurant_id}"

    # Сравниваем средний чек ресторана
    assert float(response_api_detail.data["average_check"]) == float(
        db_restaurant.average_check
    ), f"Несоответствие среднего чека для ресторана с ID {api_restaurant_id}"

    # Сравниваем описание ресторана
    assert (
        response_api_detail.data["description"] == db_restaurant.description
    ), f"Несоответствие описания для ресторана с ID {api_restaurant_id}"

