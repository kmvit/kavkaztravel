import pytest
from decimal import Decimal
from datetime import datetime

# Прямой URL для создания аренды
RENTAL_CREATE_URL = "/api/v1/kashiring/rental/create/"


def calculate_expected_rental_price(
    pickup_datetime, return_datetime, base_price_per_day, rental_discount=None
):
    """
    Рассчитывает ожидаемую общую стоимость аренды с учетом скидки.
    :param pickup_datetime: datetime - время получения
    :param return_datetime: datetime - время возврата
    :param base_price_per_day: Decimal - базовая цена за день аренды
    :param rental_discount: объект RentalDiscount или None
    :return: округленная стоимость аренды (Decimal)
    """
    rental_days = (return_datetime - pickup_datetime).days
    total_price = rental_days * base_price_per_day
    if rental_discount:
        # Метод get_discount возвращает скидку в виде дроби, например 0.05 для 5%
        discount = rental_discount.get_discount(rental_days)
        total_price *= Decimal(1 - discount)
    return round(total_price, 2)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "rental_payload",
    [
        "rental_payload_less_than_7_days",
        "rental_payload_7_days",
        "rental_payload_between_7_and_30_days",
        "rental_payload_30_days",
        "rental_payload_more_than_30_days",
    ],
)
def test_rental_price(
    rental_payload, rental_discount, api_client, user, car_1, request
):
    """
    Тест создания аренды через API для разных сроков аренды с применением скидки.
    Выводит:
      - Имя тестового payload (например, "rental_payload_7_days")
      - Отправляемые данные
      - Значения pickup_datetime и return_datetime
      - Рассчитанную ожидаемую стоимость аренды
      - Ответ API
    """
    # Аутентифицируем пользователя
    api_client.force_authenticate(user=user)

    # Получаем данные аренды из соответствующей фикстуры
    # Получаем тестовые данные
    rental_data = request.getfixturevalue(rental_payload)

    # Добавляем пользователя и скидку
    rental_data.update({"user": user.id, "discount_policy": rental_discount.id})

    # Преобразуем даты в datetime
    pickup_datetime, return_datetime = map(
        datetime.fromisoformat,
        [rental_data["pickup_datetime"], rental_data["return_datetime"]],
    )

    # Рассчитываем ожидаемую стоимость аренды
    expected_price = calculate_expected_rental_price(
        pickup_datetime, return_datetime, car_1.price_per_day, rental_discount
    )

    # Отправляем POST-запрос для создания аренды
    response = api_client.post(RENTAL_CREATE_URL, rental_data, format="json")

    # Проверяем, что аренда создана успешно и стоимость совпадает с расчетной
    assert response.status_code == 201
    assert "total_price" in response.data, "Ответ API не содержит total_price"
    assert (
        Decimal(response.data["total_price"]) == expected_price
    ), f"Ожидалось {expected_price}, но получили {response.data['total_price']}"
