import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from kashiring.models import Car, CarFeature, CarImage, RentalDiscount







@pytest.mark.django_db
def test_create_car(api_client, user, rental_discount, model_camry, brand_toyota):
    """Тест создания автомобиля через API."""
    api_client.force_authenticate(user=user)

    url = "/api/v1/kashiring/cars/"
    payload = {
        "owner": user.id,
        "brand_name": brand_toyota.name, 
        "model_name": model_camry.name,
        "body_type": "sedan",
        "year_of_production": 2023,
        "engine_power": 200,
        "drive_type": "fwd",
        "engine_type": "petrol",
        "price_per_day": "47466.43",
        "features": [{"name": "air_conditioning"}],
        "discount_policy": rental_discount.name,
    }

    response = api_client.post(url, payload, format="json")
    print(response.data, 124)
    assert response.status_code == 201

    data = response.json()
    print(data, 123)
    assert data["engine_type"] == 'petrol'
    assert data["year_of_production"] ==2023
    assert "air_conditioning" in [feature["name"] for feature in data["features"]]

    # Проводим фильтрацию по бренду и проверяем, что созданный автомобиль есть в результатах
    url_filter = f"/api/v1/kashiring/cars/?brand={brand_toyota.name}"
    filter_response = api_client.get(url_filter)

    # Проверяем, что статус успешный
    assert filter_response.status_code == 200
    car = Car.objects.get(id=data["id"])  # Получаем созданный объект Car
    # Получаем список автомобилей и проверяем, что наш созданный автомобиль присутствует
    filtered_cars = filter_response.json()
    assert len(filtered_cars) == 1  # Должен быть только один автомобиль в ответе
    assert filtered_cars[0]["id"] == car.id  # Проверяем, что этот автомобиль — тот, который мы создали

@pytest.mark.django_db
def test_update_car(api_client, user, car_1, model_camry):
    """Тест обновления автомобиля через API."""
    api_client.force_authenticate(user=user)

    url = f"/api/v1/kashiring/cars/{car_1.id}/"

    payload = {
        "price_per_day": "500.00"
    }

    response = api_client.patch(url, payload, format="json")
    assert response.status_code == 200

    data = response.json()
    assert data["price_per_day"] == "500.00"


@pytest.mark.django_db
def test_delete_car(api_client, user, car_1):
    """Тест удаления автомобиля через API."""
    api_client.force_authenticate(user=user)

    url = f"/api/v1/kashiring/cars/{car_1.id}/"

    response = api_client.delete(url)
    assert response.status_code == 204



@pytest.mark.django_db
def test_filter_cars_by_body_type(api_client, car_1, car_2):
    """Фильтрация автомобилей по типу кузова."""
    url = "/api/v1/kashiring/cars/?body_type=sedan"
    response = api_client.get(url)

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2 


@pytest.mark.django_db
def test_filter_cars_by_price_range(api_client, car_1, car_2):
    """Фильтрация автомобилей по диапазону цены."""
    url = "/api/v1/kashiring/cars/?price_per_day_min=50&price_per_day_max=500"
    response = api_client.get(url)

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert float(data[0]["price_per_day"]) == 100.00


@pytest.mark.django_db
def test_anonymous_user_cannot_edit_car(api_client, car_1):
    """Неавторизованный пользователь не может редактировать машину."""
    url = f"/api/v1/kashiring/cars/{car_1.id}/"
    data = {"brand": "Honda"}  # Пробуем изменить бренд

    response = api_client.patch(url, data, format="json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED  # Ожидаем 401 ошибку
    car_1.refresh_from_db()
    assert car_1.brand != "Honda"  # Убеждаемся, что данные не изменились

@pytest.mark.django_db
def test_list_cars(api_client, user, car_1, car_2):
    """Тест для получения списка автомобилей (метод list)."""
    api_client.force_authenticate(user=user)

    # URL для получения списка автомобилей
    url = "/api/v1/kashiring/cars/"

    # Отправляем GET-запрос для получения списка автомобилей
    response = api_client.get(url)

    # Проверяем, что статус ответа успешный
    assert response.status_code == 200

    # Получаем данные ответа
    data = response.json()

    # Проверяем, что в ответе находятся только базовые данные (согласно CarListSerializer)
    assert len(data) == 2  # Два автомобиля должны быть в списке

    # Проверяем поля, которые должны быть в ответе
    for car_data in data:
        assert "id" in car_data
        assert "brand" in car_data
        assert "year_of_production" in car_data
        assert "engine_power" in car_data
        assert "drive_type" in car_data
        assert "engine_type" in car_data
        assert "price_per_day" in car_data
        assert "first_image" in car_data  # Должно быть поле для первого изображения




@pytest.mark.django_db
def test_retrieve_car(api_client, user, car_1, car_1_images, car_1_features, car_option_1, car_equipment_1):
    """Тест для получения информации о конкретном автомобиле (метод retrieve)."""
    api_client.force_authenticate(user=user)

    # URL для получения информации о конкретном автомобиле
    url = f"/api/v1/kashiring/cars/{car_1.id}/"

    # Отправляем GET-запрос для получения данных автомобиля
    response = api_client.get(url)

    # Проверяем, что статус ответа успешный
    assert response.status_code == 200

    # Получаем данные ответа
    data = response.json()

    # Проверяем, что возвращены полные данные (согласно CarSerializer)
    assert "id" in data
    assert "owner" in data
    assert "brand" in data
    assert "body_type" in data
    assert "price_per_day" in data
    assert "features" in data
    assert "images" in data
    assert "discount_policy" in data
    assert "description" in data
    assert "options" in data
    assert "equipments" in data

    # Проверяем, что поля содержат правильные данные
    assert data["id"] == car_1.id
    assert data["owner"] == str(car_1.owner)  # Проверяем владельца, это должно быть строковое представление
    assert data["brand"]["name"] == car_1.brand.name  # Проверяем название бренда
    assert data["body_type"] == car_1.body_type  # Проверяем тип кузова
    assert float(data["price_per_day"]) == car_1.price_per_day  # Проверяем цену за день с приведение к float

    # Проверяем характеристики автомобиля
    features_data = [feature["name"] for feature in data["features"]]
    for feature in car_1.features.all():
        assert feature.name in features_data  # Проверяем, что все характеристики автомобиля присутствуют

    # Проверяем изображения автомобиля
    if car_1.images.exists():
        # Получаем полный URL изображений из ответа
        image_urls = [image["image"] for image in data["images"]]

        # Сравниваем только относительные пути
        for image in car_1.images.all():
            # Получаем относительный путь изображения
            image_path = image.image.url.replace(settings.MEDIA_URL, "")
            # Формируем полный URL с префиксом
            full_image_url = f"http://testserver{settings.MEDIA_URL}{image_path}"
            assert full_image_url in image_urls  # Проверяем, что полный URL изображения присутствует

    # Проверяем скидочную политику
    if car_1.discount_policy:
        assert data["discount_policy"]["name"] == car_1.discount_policy.name  # Проверяем название политики скидки
    else:
        assert data["discount_policy"] is None  # Если нет скидки, то должно быть None

    # Проверяем описание автомобиля
    assert data["description"] == car_1.description  # Проверяем описание

    # Проверяем дополнительные опции автомобиля
    options_data = [option["name"] for option in data["options"]]
    assert car_option_1.name in options_data  # Проверяем, что опция присутствует
    assert f"{car_option_1.price:.2f}" == f"{float(data['options'][0]['price']):.2f}"

    # Проверяем комплектации автомобиля
    equipments_data = [equipment["name"] for equipment in data["equipments"]]
    assert car_equipment_1.name in equipments_data  # Проверяем, что комплектация присутствует
