import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from restaurants.models import Restaurant, RestaurantImage, Service, RestaurantType
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()

BASE_ULR = "/api/v1/restaurants/meal/"


@pytest.mark.django_db
def test_create_restaurant(authenticated_api_client, child_region):
    """Тест создания ресторана с проверкой уникальности Service и RestaurantType"""

    # Подготовка данных
    data = {
        "name": "New Restaurant",
        "address": "Test Address",
        "region": child_region.id,
        "average_check": "2000.00",
        "description": "Test Description",
        "working_hours": "10:00-22:00",
        "restaurant_type": {"name": "Test Type", "description": "Type Description"},
        "services": [{"name": "789", "description": "wi-fi"}],
    }

    # Отправка первого запроса
    response = authenticated_api_client.post(BASE_ULR, data, format="json")

    # Проверки после первого запроса
    assert response.status_code == 201, response.data
    assert response.data["name"] == "New Restaurant"

    # Проверяем, что создался один новый ресторан
    assert Restaurant.objects.count() == 1

    # Проверяем, что создался один новый объект Service
    assert Service.objects.count() == 1

    # Проверяем, что создался один новый объект RestaurantType
    assert RestaurantType.objects.count() == 1

    # Отправляем второй запрос с теми же данными
    response = authenticated_api_client.post(BASE_ULR, data, format="json")

    # Проверки после второго запроса
    assert response.status_code == 201, response.data
    assert response.data["name"] == "New Restaurant"

    # Проверяем, что количество объектов Service и RestaurantType не изменилось
    assert Service.objects.count() == 1
    assert RestaurantType.objects.count() == 1

    # Проверяем, что добавлено только 1 ресторан
    assert Restaurant.objects.count() == 2


from decimal import Decimal


@pytest.mark.django_db
def test_update_restaurant(authenticated_api_client, restaurant, child_region):
    """Тест обновления ресторана с проверкой данных до и после обновления"""

    # Проверяем начальные данные ресторана перед обновлением
    initial_restaurant = Restaurant.objects.get(id=restaurant.id)

    assert initial_restaurant.name == "Ресторан 'Горный аул'"
    assert initial_restaurant.address == "ул. Кавказская, 15"
    assert initial_restaurant.region == child_region
    assert initial_restaurant.average_check == 1500.00
    assert initial_restaurant.description == "Лучшие блюда кавказской кухни"
    assert initial_restaurant.working_hours == "10:00-22:00"
    assert (
        initial_restaurant.restaurant_type.name == "Кавказская кухня"
    )  # предположим, что тип ресторана такой
    assert (
        initial_restaurant.services.count() == 8
    )  # Услуги должны быть добавлены через фикстуру

    # Данные для обновления
    update_data = {
        "name": "Обновленный ресторан",
        "address": "ул. Новая, 20",  # Обновленный адрес
        "region": child_region.id,
        "average_check": 2500.00,  # Новый средний чек
        "description": "Лучшие блюда кавказской и европейской кухни",  # Обновленное описание
        "working_hours": "09:00-23:00",  # Обновленные часы работы
        "restaurant_type": {
            "name": "Новый тип ресторана",
            "description": "Обновленное описание",
        },
        "services": [{"name": "789", "description": "Обновленная услуга wi-fi"}],
    }
    # Отправляем запрос на обновление
    response = authenticated_api_client.put(
        f"/api/v1/restaurants/meal/{restaurant.id}/", update_data, format="json"
    )

    # Проверяем, что данные действительно обновились в базе
    updated_restaurant = Restaurant.objects.get(id=restaurant.id)

    # Прокачиваем связанные услуги и проверяем их
    updated_services = (
        updated_restaurant.services.all()
    )  # Получаем все связанные услуги
    assert updated_services.count() == 1  # Убедитесь, что услуга была обновлена

    # Теперь проверяем атрибуты связанной услуги
    updated_service = (
        updated_services.first()
    )  # Получаем первую услугу (поскольку это one-to-many)
    assert updated_service.name == "789"  # Проверяем, что имя услуги обновилось
    assert (
        updated_service.description == "Обновленная услуга wi-fi"
    )  # Проверяем описание услуги

    # Проверяем обновленные поля ресторана
    assert updated_restaurant.name == "Обновленный ресторан"
    assert updated_restaurant.address == "ул. Новая, 20"
    assert updated_restaurant.average_check == 2500.00
    assert (
        updated_restaurant.description == "Лучшие блюда кавказской и европейской кухни"
    )
    assert updated_restaurant.working_hours == "09:00-23:00"
    assert updated_restaurant.restaurant_type.name == "Новый тип ресторана"


@pytest.mark.django_db
def test_delete_restaurant(authenticated_api_client, restaurant):
    """Тест удаления ресторана"""

    # Получаем ID ресторана для отправки запроса на удаление
    restaurant_id = restaurant.id

    # Отправляем запрос на удаление ресторана
    response = authenticated_api_client.delete(
        f"/api/v1/restaurants/meal/{restaurant_id}/"
    )

    # Проверки на успешное удаление
    assert (
        response.status_code == 204
    ), f"Expected 204, but got {response.status_code}"  # Ожидаем статус 204 No Content

    # Проверяем, что ресторан был удален из базы данных
    assert not Restaurant.objects.filter(
        id=restaurant_id
    ).exists(), "Restaurant was not deleted"


@pytest.mark.django_db
def test_restaurant_list_with_pagination_and_fields_check(
    authenticated_api_client, owner, restaurant, child_region, restaurant_image_1
):
    """
    Тест для проверки метода list с пагинацией, полями и изображениями.
    Для каждого ресторана (включая фикстурный) добавляем изображение через фикстуру restaurant_image_1.
    Создаем 23 новых ресторанов (итого 8) и проверяем, что пагинация работает корректно,
    а в данных присутствуют необходимые поля.
    """

    # Для ресторана из фикстуры добавляем изображение

    # Создаем 23 новых ресторанов
    for i in range(23):
        r_type = RestaurantType.objects.create(
            name=f"Тип ресторана {i+1}", description=f"Описание типа {i+1}"
        )
        serv = Service.objects.create(
            name=f"Услуга {i+1}", description=f"Описание услуги {i+1}"
        )
        new_rest = Restaurant.objects.create(
            name=f"Ресторан {i+1}",
            address=f"ул. Адрес {i+1}",
            region=child_region,
            owner=owner,
            average_check="1500.00",
            description=f"Описание ресторана {i+1}",
            working_hours="10:00-22:00",
            restaurant_type=r_type,
        )
        # Используем фикстуру для добавления изображения
        image_file = SimpleUploadedFile(
            "test_image_3.jpg", b"image_data", content_type="image/jpeg"
        )
        RestaurantImage.objects.create(restaurant=new_rest, image=image_file)
        new_rest.services.add(serv)

    # Отправляем запрос на получение списка ресторанов (пагинация: 20 на страницу)
    response = authenticated_api_client.get(BASE_ULR, {"page": 1}, format="json")

    # Проверяем статус ответа
    assert (
        response.status_code == status.HTTP_200_OK
    ), f"Expected 200, got {response.status_code}"

    # Проверяем количество ресторанов
    assert response.data.get("count") == 24, "Total count of restaurants should be 8"

    # Проверяем пагинацию: 5 ресторанов на первой странице
    results = response.data.get("results", [])
    assert len(results) == 20, "Expected 20 restaurants on page 1"

    # Проверяем ссылки пагинации
    assert (
        "next" in response.data and response.data["next"] is not None
    ), "'next' pagination link should be present"
    assert (
        "previous" in response.data and response.data["previous"] is None
    ), "'previous' should be None on first page"

    # Проверяем поля для первого ресторана на первой странице
    rest_data = results[1]

    # Проверка обязательных полей и значений
    assert "id" in rest_data, "Restaurant 'id' should be present"
    assert isinstance(rest_data["id"], int), "Restaurant 'id' should be an integer"

    assert "name" in rest_data, "Restaurant 'name' should be present"
    assert rest_data["name"] == "Ресторан 1", "Restaurant 'name' should be 'Ресторан 1'"

    assert "region" in rest_data, "Restaurant 'region' should be present"
    assert rest_data["region"] == str(
        child_region
    ), f"Restaurant 'region' should be {child_region}"

    assert (
        "short_description" in rest_data
    ), "Restaurant 'short_description' should be present"
    assert (
        rest_data["short_description"] == "Описание ресторана 1..."
    ), "Restaurant 'short_description' should match"

    assert (
        "restaurant_type" in rest_data
    ), "Restaurant 'restaurant_type' should be present"
    assert (
        rest_data["restaurant_type"]["name"] == "Тип ресторана 1"
    ), "Restaurant type name should be 'Тип ресторана 1'"

    assert "services" in rest_data, "Restaurant 'services' should be present"
    services = rest_data["services"]
    assert isinstance(services, list), "Services should be a list"
    assert len(services) == 1, "There should be 1 service for this restaurant"
    assert services[0]["name"] == "Услуга 1", "Service name should be 'Услуга 1'"

    assert "main_image" in rest_data, "Restaurant 'main_image' should be present"
    main_image = rest_data["main_image"]
    assert isinstance(
        main_image, str
    ), "Main image should be a string (URL or file path)"
    assert main_image != "", "Main image should not be empty"

    assert "average_check" in rest_data, "Restaurant 'average_check' should be present"
    assert (
        rest_data["average_check"] == "1500.00"
    ), "Restaurant 'average_check' should be '1500.00'"

    # Проверяем пагинацию: вторая страница должна содержать 3 ресторана (24 - 20 = 4)
    response_page_2 = authenticated_api_client.get(BASE_ULR, {"page": 2}, format="json")
    assert (
        response_page_2.status_code == status.HTTP_200_OK
    ), f"Expected 200, got {response_page_2.status_code}"
    results_page_2 = response_page_2.data.get("results", [])
    assert len(results_page_2) == 4, "Expected 3 restaurants on page 2"


@pytest.mark.django_db
def test_filter_by_region(
    authenticated_api_client, restaurants, child_region, additional_regions
):
    """Тест для фильтрации ресторанов по региону."""
    # Фильтруем по региону "Москва"
    response = authenticated_api_client.get(
        BASE_ULR, {"region": "Москва"}, format="json"
    )
    assert (
        response.status_code == status.HTTP_200_OK
    ), f"Expected 200, got {response.status_code}"

    # Подсчитываем рестораны, относящиеся к Москве
    expected_count = sum(
        1 for restaurant in restaurants if restaurant.region.name == "Москва"
    )
    print(expected_count)
    # Проверяем, что количество ресторанов в ответе совпадает с ожидаемым
    assert (
        response.data["count"] == expected_count
    ), f"Expected {expected_count} restaurants, got {response.data['count']}"


@pytest.mark.django_db
def test_filter_by_average_check(authenticated_api_client, restaurants):
    """Тест для фильтрации ресторанов по среднему чеку."""
    # Фильтруем рестораны с average_check >= 2000
    response = authenticated_api_client.get(
        BASE_ULR, {"average_check_min": 2000}, format="json"
    )
    assert (
        response.status_code == status.HTTP_200_OK
    ), f"Expected 200, got {response.status_code}"

    # Подсчитываем рестораны, где average_check >= 2000
    expected_count = sum(
        1 for restaurant in restaurants if restaurant.average_check >= 2000
    )
    print(expected_count)
    # Проверяем, что количество ресторанов в ответе совпадает с ожидаемым
    assert (
        response.data["count"] == expected_count
    ), f"Expected {expected_count} restaurants, got {response.data['count']}"


@pytest.mark.django_db
def test_filter_by_service(authenticated_api_client, restaurants, services):
    """Тест для фильтрации ресторанов по услугам."""
    # Фильтруем рестораны, у которых есть услуга "Шашлык"
    response = authenticated_api_client.get(
        BASE_ULR, {"services": "Шашлык"}, format="json"
    )
    assert (
        response.status_code == status.HTTP_200_OK
    ), f"Expected 200, got {response.status_code}"

    # Подсчитываем рестораны, которые имеют услугу "Шашлык"
    expected_count = sum(
        1
        for restaurant in restaurants
        if "Шашлык" in [service.name for service in restaurant.services.all()]
    )
    print(expected_count)
    # Проверяем, что количество ресторанов в ответе совпадает с ожидаемым
    assert (
        response.data["count"] == expected_count
    ), f"Expected {expected_count} restaurants, got {response.data['count']}"


@pytest.mark.django_db
def test_filter_by_restaurant_type(authenticated_api_client, restaurants):
    """Тест для фильтрации ресторанов по типу."""
    # Фильтруем рестораны типа "Кавказская кухня"
    response = authenticated_api_client.get(
        BASE_ULR,
        {"restaurant_type": "Кавказская кухня"},
        format="json",
    )
    assert (
        response.status_code == status.HTTP_200_OK
    ), f"Expected 200, got {response.status_code}"

    # Подсчитываем рестораны, которые имеют тип "Кавказская кухня"
    expected_count = sum(
        1
        for restaurant in restaurants
        if restaurant.restaurant_type.name == "Кавказская кухня"
    )
    print(expected_count)
    # Проверяем, что количество ресторанов в ответе совпадает с ожидаемым
    assert (
        response.data["count"] == expected_count
    ), f"Expected {expected_count} restaurants, got {response.data['count']}"


@pytest.mark.django_db
def test_filter_by_restaurant_type_and_service(authenticated_api_client, restaurants):
    """Тест для фильтрации ресторанов по типу и услуге."""
    # Фильтруем рестораны типа "Итальянская кухня" и услуги "Паста"
    response = authenticated_api_client.get(
        BASE_ULR,
        {"restaurant_type": "Итальянская кухня", "services": "Паста"},
        format="json",
    )

    assert (
        response.status_code == status.HTTP_200_OK
    ), f"Expected 200, got {response.status_code}"

    # Подсчитываем рестораны, которые имеют тип "Итальянская кухня" и услугу "Паста"
    expected_count = sum(
        1
        for restaurant in restaurants
        if restaurant.restaurant_type.name == "Итальянская кухня"
        and "Паста" in [service.name for service in restaurant.services.all()]
    )

    # Проверяем, что количество ресторанов в ответе совпадает с ожидаемым
    assert (
        response.data["count"] == expected_count
    ), f"Expected {expected_count} restaurants, got {response.data['count']}"


@pytest.mark.django_db
def test_retrieve_restaurant(
    authenticated_api_client, restaurant, restaurant_image_1, services
):
    """Тест проверяет, что метод retrieve возвращает ресторан с корректными полями."""

    response = authenticated_api_client.get(
        f"/api/v1/restaurants/meal/{restaurant.id}/", format="json"
    )

    assert (
        response.status_code == status.HTTP_200_OK
    ), f"Expected 200, got {response.status_code}"

    data = response.json()
    # Проверка основных полей
    assert data["id"] == restaurant.id, "ID ресторана должен совпадать"
    assert data["name"] == restaurant.name, "Название ресторана должно совпадать"
    assert data["address"] == restaurant.address, "Адрес ресторана должен совпадать"
    assert data["region"] == restaurant.region.id, "ID региона должен совпадать"
    assert (
        data["average_check"] == f"{restaurant.average_check:.2f}"
    ), "Средний чек должен совпадать и быть строкой"
    assert (
        data["description"] == restaurant.description
    ), "Описание ресторана должно совпадать"
    assert (
        data["working_hours"] == restaurant.working_hours
    ), "Часы работы должны совпадать"

    # Проверка объекта restaurant_type
    assert isinstance(
        data["restaurant_type"], dict
    ), "restaurant_type должен быть объектом"
    assert (
        data["restaurant_type"]["id"] == restaurant.restaurant_type.id
    ), "ID типа ресторана должен совпадать"
    assert (
        data["restaurant_type"]["name"] == restaurant.restaurant_type.name
    ), "Название типа ресторана должно совпадать"
    assert (
        data["restaurant_type"]["description"] == restaurant.restaurant_type.description
    ), "Описание типа ресторана должно совпадать"

    # Проверка списка услуг
    assert isinstance(data["services"], list), "services должен быть списком"
    assert (
        len(data["services"]) == restaurant.services.count()
    ), "Количество услуг должно совпадать"
    for service in data["services"]:
        assert isinstance(
            service, dict
        ), "Каждый элемент в services должен быть объектом"
        assert "id" in service and isinstance(
            service["id"], int
        ), "service.id должен быть числом"
        assert "name" in service and isinstance(
            service["name"], str
        ), "service.name должен быть строкой"
        assert isinstance(service["description"], (str, type(None)))
        assert any(
            s.id == service["id"] for s in restaurant.services.all()
        ), "ID услуги должен быть в списке услуг ресторана"

    # Проверка списка изображений
    assert isinstance(data["images"], list), "images должен быть списком"
    assert (
        len(data["images"]) == restaurant.images.count()
    ), "Количество изображений должно совпадать"
    for image in data["images"]:
        assert isinstance(image, dict), "Каждый элемент в images должен быть объектом"
        assert "id" in image and isinstance(
            image["id"], int
        ), "image.id должен быть числом"
        assert (
            "image" in image
            and isinstance(image["image"], str)
            and image["image"].startswith("http")
        ), "image.image должен быть URL-строкой"
        assert (
            "restaurant" in image and image["restaurant"] == restaurant.id
        ), "image.restaurant должен совпадать с ID ресторана"


from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import pytest


@pytest.mark.django_db
def test_upload_restaurant_image(authenticated_api_client, restaurant):
    """Тестируем создание изображения для ресторана"""

    # Создаем изображение в памяти с помощью Pillow
    image = BytesIO()
    img = Image.new(
        "RGB", (100, 100), color="red"
    )  # Создаем изображение 100x100 пикселей
    img.save(image, "JPEG")
    image.seek(0)  # Перемещаем указатель в начало файла, чтобы его можно было прочитать

    # Преобразуем в InMemoryUploadedFile для корректной отправки
    image_file = InMemoryUploadedFile(
        image,  # Источник данных (в памяти)
        None,  # Объект формы, может быть None
        "image.jpg",  # Имя файла
        "image/jpeg",  # Тип контента
        image.tell(),  # Размер файла в байтах
        None,  # Оставляем None для проверки в некоторых случаях
    )

    # Отправляем запрос для создания изображения
    response = authenticated_api_client.post(
        "/api/v1/restaurants/restaurant-images/",  # URL для создания изображения
        {"restaurant": restaurant.id, "image": image_file},
        format="multipart",  # Указываем формат передачи файлов
    )

    # Проверяем, что ответ был успешным и код состояния 201 (создано)
    assert (
        response.status_code == 201
    ), f"Expected 201, got {response.status_code}. Response: {response.data}"

    # Дополнительно можно проверить, что возвращенные данные содержат корректную информацию о загруженном изображении
    assert "id" in response.data, "Response should contain an 'id' field"
    assert "image" in response.data, "Response should contain an 'image' field"
    assert response.data["image"] is not None, "Image URL should not be null"
