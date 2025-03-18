import pytest
from datetime import datetime
from decimal import Decimal
from django.contrib.auth import get_user_model

# Прямой URL для создания аренды
RENTAL_CREATE_URL = "/api/v1/kashiring/rental/create/"


@pytest.fixture
def owner(db):
    """Фикстура для пользователя-владельца."""
    User = get_user_model()
    return User.objects.create_user(
        username="owner_user", password="password123", email="owner@example.com"
    )


@pytest.fixture
def user(db):
    """Фикстура для арендатора."""
    User = get_user_model()
    return User.objects.create_user(
        username="renter_user", password="password123", email="renter@example.com"
    )


@pytest.mark.django_db
def test_rental_process_with_discounts(api_client, owner, user, rental_discount):
    """Тест полного цикла аренды автомобиля с учетом скидок."""

    # 1. Владелец создает несколько машин
    api_client.force_authenticate(user=owner)

    cars_data = [
        {
            "owner": owner.id,
            "brand_name": "Toyota",
            "model_name": "Camry",
            "price_per_day": 5000,
            "body_type": "sedan",
            "year_of_production": 2023,
            "engine_power": 200,
            "drive_type": "fwd",
            "engine_type": "petrol",
            "features": [{"name": "air_conditioning"}],
            "discount_policy": rental_discount.name,
        },
        {
            "owner": owner.id,
            "brand_name": "Toyota",
            "model_name": "Corolla",
            "price_per_day": 3000,
            "body_type": "sedan",
            "year_of_production": 2022,
            "engine_power": 150,
            "drive_type": "fwd",
            "engine_type": "diesel",
            "features": [{"name": "sunroof"}],
            "discount_policy": rental_discount.name,
        },
        {
            "owner": owner.id,
            "brand_name": "Kia",
            "model_name": "Rio",
            "price_per_day": 2000,
            "body_type": "hatchback",
            "year_of_production": 2021,
            "engine_power": 130,
            "drive_type": "fwd",
            "engine_type": "petrol",
            "features": [{"name": "air_conditioning"}],
            "discount_policy": rental_discount.name,
        },
        {
            "owner": owner.id,
            "brand_name": "Kia",
            "model_name": "Sportage",
            "price_per_day": 4500,
            "body_type": "suv",
            "year_of_production": 2020,
            "engine_power": 170,
            "drive_type": "awd",
            "engine_type": "diesel",
            "features": [{"name": "sunroof"}],
            "discount_policy": rental_discount.name,
        },
    ]

    created_cars = []
    for car_data in cars_data:
        response = api_client.post("/api/v1/kashiring/cars/", car_data, format="json")
        assert (
            response.status_code == 201
        ), f"Ошибка при создании машины: {response.content}"
        data = response.json()
        created_cars.append(data)

    # 2. Фильтруем машины по бренду Kia и цене в диапазоне от 4200 до 4800 и проверяем, что созданные машины присутствуют
    url_filter = f"/api/v1/kashiring/cars/?brand=Kia&price_per_day_min=4200&price_per_day_max=4800"
    filter_response = api_client.get(url_filter)
    assert (
        filter_response.status_code == 200
    ), f"Ошибка при фильтрации машин: {filter_response.content}"

    filtered_cars = filter_response.json()
    assert (
        len(filtered_cars) == 1
    )  # Ожидаем 1 машину марки Kia (Sportage), которая стоит в пределах от 4200 до 4800

    # 3. Осуществляем аренду автомобиля с учётом скидки (срок аренды = 10 дней)
    car_to_rent = created_cars[3]  # Арендуем машину Kia Sportage
    rental_data = {
        "car": car_to_rent["id"],  # ID арендованной машины
        "renter": user.id,  # Арендатор
        "user": user.id,  # Повторно арендатор
        "pickup_datetime": "2025-03-20T14:22:59.765000Z",  # Время начала аренды
        "return_datetime": "2025-03-30T14:22:59.765000Z",  # Время окончания аренды (10 дней)
    }

    rental_url = "/api/v1/kashiring/rental/create/"
    rental_response = api_client.post(rental_url, rental_data, format="json")

    assert (
        rental_response.status_code == 201
    ), f"Ошибка при аренде автомобиля: {rental_response.content}"

    rental_data_response = rental_response.json()

    # 4. Проверяем стоимость аренды с учетом скидки
    price_per_day = Decimal(car_to_rent["price_per_day"])

    # Преобразуем строки с датами в объекты datetime
    pickup_datetime = datetime.fromisoformat(
        rental_data["pickup_datetime"].replace("Z", "+00:00")
    )
    return_datetime = datetime.fromisoformat(
        rental_data["return_datetime"].replace("Z", "+00:00")
    )

    # Считаем количество дней аренды (10 дней)
    rental_days = (return_datetime - pickup_datetime).days

    expected_price_without_discount = (
        price_per_day * rental_days
    )  # общая стоимость без скидки

    # Если есть скидка, применяем ее с использованием метода get_discount
    discount_percentage = rental_discount.get_discount(
        rental_days
    )  # получаем скидку в виде десятичной дроби

    # Преобразуем discount_percentage в Decimal для корректных расчетов
    discount_percentage = Decimal(discount_percentage)

    # Вычисляем стоимость с учетом скидки
    expected_price_with_discount = expected_price_without_discount * (
        1 - discount_percentage
    )

    # Округляем к 2 знакам после запятой для точности
    expected_price_with_discount = round(expected_price_with_discount, 2)

    # Проверяем, что в ответе аренды указана правильная сумма
    actual_total_price = Decimal(rental_data_response["total_price"])
    actual_total_price = round(actual_total_price, 2)  # Округляем до 2 знаков
    assert (
        actual_total_price == expected_price_with_discount
    ), f"Ошибка в расчете стоимости аренды. Ожидалось: {expected_price_with_discount}, получено: {actual_total_price}"

    # 5. Проверяем, что арендованной машины больше нет в списке доступных машин
    filter_response_after_rental = api_client.get(url_filter)
    assert filter_response_after_rental.status_code == 200

    filtered_cars_after_rental = filter_response_after_rental.json()

    # В списке доступных автомобилей больше не должно быть арендованной машины
    assert (
        len(filtered_cars_after_rental) == 0
    )  # Машины с брендом Kia и ценой в пределах от 4200 до 4800 больше нет

    # Убедимся, что арендованная машина была удалена из доступных
    remaining_car_ids = [car["id"] for car in filtered_cars_after_rental]
    assert (
        car_to_rent["id"] not in remaining_car_ids
    )  # Проверяем, что арендованная машина исчезла
