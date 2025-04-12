import pytest
from rest_framework import status
from django.urls import reverse
from tours.models import Tour, TagTour
from regions.models import Region
from rest_framework.test import APIClient

# Общий URL для тестов
url = "/api/v1/tours/current/"


@pytest.mark.django_db
def test_create_tour(api_client, user, region, tag):
    """Тест создания нового тура"""
    data = {
        "title": "Новый тур",
        "description": "Описание нового тура",
        "terms": "Условия нового тура",
        "region": region.id,
        "price": 1500,
        "tags": [tag.id],  # Используем имена тегов
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    # Проверка, что тур создан
    tour = Tour.objects.get(id=response.data["id"])
    assert tour.title == "Новый тур"
    assert tour.description == "Описание нового тура"
    assert tour.price == 1500
    assert tour.tags.first().name == "Пешеходный"  # Проверка имени тега


import pytest
from rest_framework import status


@pytest.mark.django_db
def test_list_tours(api_client, tour):
    """Тест получения списка туров"""
    response = api_client.get(url, format="json")

    # Проверка статуса ответа
    assert response.status_code == status.HTTP_200_OK

    results = response.data["results"]

    # Проверка, что хотя бы один тур вернулся
    # Проверка, что нужный тур есть среди результатов
    titles = [item["title"] for item in results]
    assert tour.title in titles


import pytest
from rest_framework import status


@pytest.mark.django_db
def test_update_tour(api_client, tour, tag):
    """Тест обновления тура"""
    updated_data = {
        "guide": tour.guide.id,  # Указываем guide, как идентификатор пользователя, который является гидом
        "region": tour.region.id,  # Указываем region, как идентификатор региона
        "title": "Обновленный тур",
        "description": "Новое описание",
        "terms": "Новые условия",
        "price": "15000.00",
        "tags": [tag.id],  # Используем ID тега вместо его имени
    }

    base_url = "/api/v1/tours/current/"
    request_url = f"{url}{tour.id}/"

    response = api_client.put(request_url, updated_data, format="json")

    assert (
        response.status_code == status.HTTP_200_OK
    ), f"Ошибка обновления, ответ: {response.data}"

    # Обновляем объект из базы и выводим его для отладки
    tour.refresh_from_db()

    # Проверяем, что данные обновились корректно
    assert tour.title == "Обновленный тур"
    assert tour.description == "Новое описание"
    assert tour.price == 15000.00


@pytest.mark.django_db
def test_delete_tour(api_client, tour):
    """Тест удаления тура"""
    response = api_client.delete(
        reverse("tour-detail", kwargs={"pk": tour.id}), format="json"
    )

    # Проверка статуса ответа
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Проверка, что тур удален
    with pytest.raises(Tour.DoesNotExist):
        Tour.objects.get(id=tour.id)


import pytest
from rest_framework import status


@pytest.mark.django_db
def test_filter_by_tags_and(api_client, tours, tags):
    """Тест фильтрации туров по тегам с логикой AND."""
    # Запрос с фильтрацией по тегам 'Горный' и 'Пешеходный' (оба тега должны быть у тура)
    response = api_client.get(
        url, {"tags": [tags[0].id, tags[1].id], "tags_mode": "AND"}
    )

    assert response.status_code == status.HTTP_200_OK

    # Проверяем, что найден только один тур
    assert response.data["count"] == 1
    assert len(response.data["results"]) == 1

    tour = response.data["results"][0]
    assert tour["title"] == "Горный тур в Алтай"


@pytest.mark.django_db
def test_filter_by_tags_or(api_client, tours, tags):
    """Тест фильтрации туров по тегам с логикой OR."""
    # Запрос с фильтрацией по тегам 'Горный' или 'Пешеходный' (должен вернуть все туры с хотя бы одним из этих тегов)
    response = api_client.get(
        url, {"tags": [tags[0].id, tags[1].id], "tags_mode": "OR"}
    )

    assert response.status_code == status.HTTP_200_OK

    # Проверяем, что вернулось два результата
    assert response.data["count"] == 2
    assert len(response.data["results"]) == 2

    # Проверяем, что нужные туры действительно в ответе
    titles = [tour["title"] for tour in response.data["results"]]
    assert "Горный тур в Алтай" in titles
    assert "Пешеходный тур" in titles


@pytest.mark.django_db
def test_filter_by_price_range(api_client, tours):
    """Тест фильтрации туров по цене в диапазоне."""
    # Запрос с фильтрацией по цене от 8000 до 10000
    response = api_client.get(url, {"price_min": 8000, "price_max": 10000})
    assert response.data["count"] == 3
    assert len(response.data["results"]) == 3


@pytest.mark.django_db
def test_filter_by_region(api_client, tours, region):
    """Тест фильтрации туров по региону."""
    response = api_client.get(url, {"region": region.id})

    assert response.status_code == status.HTTP_200_OK

    results = response.data["results"]
    assert len(results) == 4  # Все туры должны быть возвращены
    assert all(tour["region"] == region.id for tour in results)


@pytest.mark.django_db
def test_filter_by_non_existing_region(api_client, tours, child_region):
    """Тест фильтрации туров по несуществующему региону."""

    # Создаем новый регион, которого нет среди существующих туров
    new_region = Region.objects.create(name="Не существующий регион", url="pckpack")
    from rest_framework.test import APIClient

    # Запрос с фильтрацией по региону "Не существующий регион", которого нет среди туров
    response = api_client.get(url, {"region": new_region.id})
    # Проверяем, что ответ имеет статус 200 OK
    assert response.data["count"] == 0
    assert response.data["results"] == []


@pytest.mark.django_db
def test_get_tour_permissions_read_only(tour, user, api_client):
    """Тест доступа к туру для всех пользователей (READ-ONLY)."""

    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get(f"{url}{tour.id}/")
    assert response.status_code == status.HTTP_200_OK

    # Тест для владельца
    response = api_client.get(f"{url}{tour.id}/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_patch_tour_permissions_owner(api_client, owner, user, tour):
    """Тест прав на PATCH для владельца и другого пользователя."""

    # Владелец может редактировать
    updated_data = {"title": "Обновленный горный тур"}
    response = api_client.patch(f"{url}{tour.id}/", updated_data)
    assert response.status_code == status.HTTP_200_OK

    # Другой пользователь не может редактировать
    client = APIClient()
    client.force_authenticate(user=user)
    updated_data = {"title": "Обновленный горный тур"}
    response = client.patch(f"{url}{tour.id}/", updated_data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_create_tour_with_non_existent_tag(api_client, owner, region):
    """Тест создания нового тура с несуществующим тегом"""
    # Создаем несуществующий ID тега
    non_existent_tag_id = 99999  # предположим, что этот тег не существует в базе данных

    # Данные для запроса с несуществующим тегом
    data = {
        "title": "Новый тур с несуществующим тегом",
        "description": "Описание нового тура с несуществующим тегом",
        "terms": "Условия нового тура",
        "region": region.id,
        "price": 1500,
        "tags": [non_existent_tag_id],  # Используем несуществующий тег
    }

    # Отправляем запрос на создание тура
    response = api_client.post(url, data, format="json")
    # Проверяем, что статус ответа - ошибка 400 (плохой запрос)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Проверяем, что сообщение об ошибке соответствует ожиданиям
    assert "Тег с ID 99999 не существует!" in str(response.data)


@pytest.mark.django_db
def test_create_tour_with_invalid_price(api_client, user, region, tag):
    """Тест создания тура с отрицательной ценой"""
    data = {
        "title": "Невалидный тур",
        "description": "Плохая цена",
        "terms": "Условия",
        "region": region.id,
        "price": -1000,
        "tags": [tag.id],
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "price" in response.data


import pytest
from rest_framework import status


@pytest.mark.django_db
def test_tour_list_pagination(api_client, tours):
    """Тест пагинации списка туров с использованием PageNumberPagination."""
    # Поскольку у нас custom пагинатор TourPagination установил page_size по умолчанию 20,
    # мы явно укажем page_size=2, чтобы получить 2 объекта на странице,
    # а page=1 — первую страницу.
    response = api_client.get(url, {"page_size": 2, "page": 1})
    assert response.status_code == status.HTTP_200_OK
    assert "results" in response.data

    # Проверяем, что на первой странице ровно 2 тура
    assert len(response.data["results"]) == 2

    # Проверяем общее количество туров, которое должно совпадать с количеством в тестовой фикстуре
    # Если в тесте tours 4 объекта, то count должен быть равен 4.
    assert response.data["count"] == len(tours)


import pytest
from rest_framework import status
from tours.models import Tour
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_my_tours(api_client, owner, user, tags, region):
    """Тест для получения только своих туров (по текущему гиду)."""

    # Создаем по несколько туров для каждого пользователя
    tour_owner_1 = Tour.objects.create(
        guide=owner,
        title="Горный тур в Алтай",
        description="Тур по горам Алтая",
        region=region,
        price=12000.00,
    )
    tour_owner_2 = Tour.objects.create(
        guide=owner,
        title="Пешеходный тур по Алтаю",
        description="Тур для любителей пеших прогулок",
        region=region,
        price=10000.00,
    )

    tour_user_1 = Tour.objects.create(
        guide=user,
        title="Летний тур по Алтаю",
        description="Летний тур по Алтаю",
        region=region,
        price=8000.00,
    )
    tour_user_2 = Tour.objects.create(
        guide=user,
        title="Культурный тур по Санкт-Петербургу",
        description="Тур по историческим местам Санкт-Петербурга",
        region=region,
        price=9000.00,
    )

    # Авторизация пользователя как владельца (гид)
    api_client.force_authenticate(user=owner)

    # Запрос на получение туров текущего гида (owner)
    response = api_client.get("/api/v1/tours/current/my_tours/")

    # Проверяем, что статус ответа - 200 OK
    assert response.status_code == status.HTTP_200_OK

    # Проверяем, что возвращаются только туры владельца (owner)
    assert response.data["count"] == 2  # Только два тура от владельца
    tour_titles = [tour["title"] for tour in response.data["results"]]
    assert "Горный тур в Алтай" in tour_titles
    assert "Пешеходный тур по Алтаю" in tour_titles
    assert "Летний тур по Алтаю" not in tour_titles
    assert "Культурный тур по Санкт-Петербургу" not in tour_titles

    # Авторизация другого пользователя как арендатора (user)
    api_client.force_authenticate(user=user)

    # Запрос на получение туров текущего гида (user)
    response = api_client.get("/api/v1/tours/current/my_tours/")

    # Проверяем, что статус ответа - 200 OK
    assert response.status_code == status.HTTP_200_OK

    # Проверяем, что возвращаются только туры другого пользователя (user)
    assert response.data["count"] == 2  # Только два тура от пользователя
    tour_titles = [tour["title"] for tour in response.data["results"]]
    assert "Летний тур по Алтаю" in tour_titles
    assert "Культурный тур по Санкт-Петербургу" in tour_titles
    assert "Горный тур в Алтай" not in tour_titles
    assert "Пешеходный тур по Алтаю" not in tour_titles


@pytest.mark.django_db
def test_my_tours_no_tours(api_client, owner):
    """Тест для случая, когда у гида нет туров."""

    # Авторизация пользователя как владельца (гид)
    api_client.force_authenticate(user=owner)

    # Запрос на получение туров текущего гида, но у него нет туров
    response = api_client.get("/api/v1/tours/current/my_tours/")

    # Проверяем, что статус ответа - 200 OK
    assert response.status_code == status.HTTP_200_OK

    # Проверяем, что возвращается пустой список
    assert response.data["count"] == 0
    assert len(response.data["results"]) == 0


@pytest.mark.django_db
def test_my_tours_other_user(api_client, user, tours):
    """Тест для того, чтобы проверка другого пользователя не возвращала туры другого гида."""

    # Авторизация пользователя как не владельца (не гид)
    api_client.force_authenticate(user=user)

    # Запрос на получение туров для текущего пользователя (не владельца)
    response = api_client.get("/api/v1/tours/current/my_tours/")

    # Проверяем, что статус ответа - 200 OK
    assert response.status_code == status.HTTP_200_OK

    # Проверяем, что возвращаются только туры текущего пользователя (гида)
    assert response.data["count"] == 0  # Туры текущего пользователя должны быть пустыми
    assert len(response.data["results"]) == 0
