import pytest
from rest_framework.test import APIClient

# Прямой путь для всех тестов
rental_create_url = '/api/v1/kashiring/rental/create/'
import pytest

@pytest.mark.django_db
def test_rental_price_less_than_7_days(rental_payload_less_than_7_days, rental_discount, api_client, user):
    """Тест для аренды на меньше чем 7 дней."""
    api_client.force_authenticate(user=user)  # Аутентификация пользователя
    
    # Добавляем поле user в тело запроса
    rental_payload_less_than_7_days["user"] = user.id  # Добавляем ID пользователя

    # Выводим запрос для отладки
    print(rental_payload_less_than_7_days)

    response = api_client.post("/api/v1/kashiring/rental/create/", rental_payload_less_than_7_days, format="json")

    # Выводим ошибку для отладки
    print(response.data)

    assert response.status_code == 201  # Проверяем успешное создание


@pytest.mark.django_db
def test_rental_price_7_days(rental_payload_7_days, api_client, user):
    """Тест для аренды на 7 дней."""
    api_client.force_authenticate(user=user)  # Аутентификация пользователя

    # Добавляем поле user в тело запроса
    rental_payload_7_days["user"] = user.id  # Добавляем ID пользователя

    # Выводим запрос для отладки
    print(rental_payload_7_days)

    response = api_client.post("/api/v1/kashiring/rental/create/", rental_payload_7_days, format="json")

    # Выводим ошибку для отладки
    print(response.data)

    assert response.status_code == 201  # Проверяем успешное создание


@pytest.mark.django_db
def test_rental_price_between_7_and_30_days(rental_payload_between_7_and_30_days, rental_discount, api_client, user):
    """Тест для аренды от 7 до 30 дней."""
    api_client.force_authenticate(user=user)  # Аутентификация пользователя
    
    # Добавляем поле user в тело запроса
    rental_payload_between_7_and_30_days["user"] = user.id  # Добавляем ID пользователя
    rental_payload_between_7_and_30_days["discount_policy"] = rental_discount.id  # Применяем скидку

    # Выводим запрос для отладки
    print(rental_payload_between_7_and_30_days)

    response = api_client.post("/api/v1/kashiring/rental/create/", rental_payload_between_7_and_30_days, format="json")

    # Выводим ошибку для отладки
    print(response.data)

    assert response.status_code == 201  # Проверяем успешное создание


@pytest.mark.django_db
def test_rental_price_30_days(rental_payload_30_days, rental_discount, api_client, user):
    """Тест для аренды на 30 дней с недельной и месячной скидкой."""
    api_client.force_authenticate(user=user)  # Аутентификация пользователя

    # Добавляем поле user в тело запроса
    rental_payload_30_days["user"] = user.id  # Добавляем ID пользователя
    rental_payload_30_days["discount_policy"] = rental_discount.id  # Применяем скидку

    # Выводим запрос для отладки
    print(rental_payload_30_days)

    response = api_client.post("/api/v1/kashiring/rental/create/", rental_payload_30_days, format="json")

    # Выводим ошибку для отладки
    print(response.data)

    assert response.status_code == 201  # Проверяем успешное создание


@pytest.mark.django_db
def test_rental_price_more_than_30_days(rental_payload_more_than_30_days, rental_discount, api_client, user):
    """Тест для аренды более 30 дней с недельной и месячной скидкой."""
    api_client.force_authenticate(user=user)  # Аутентификация пользователя

    # Добавляем поле user в тело запроса
    rental_payload_more_than_30_days["user"] = user.id  # Добавляем ID пользователя
    rental_payload_more_than_30_days["discount_policy"] = rental_discount.id  # Применяем скидку

    # Выводим запрос для отладки
    print(rental_payload_more_than_30_days)

    response = api_client.post("/api/v1/kashiring/rental/create/", rental_payload_more_than_30_days, format="json")

    # Выводим ошибку для отладки
    print(response.data)

    assert response.status_code == 201  # Проверяем успешное создание


@pytest.mark.django_db
def test_rental_price_with_discount_less_than_7_days(rental_payload_less_than_7_days, rental_discount, api_client, user):
    """Тест для аренды на меньше чем 7 дней с применением скидки."""
    api_client.force_authenticate(user=user)  # Аутентификация пользователя
    
    # Добавляем поле user в тело запроса
    rental_payload_less_than_7_days["user"] = user.id  # Добавляем ID пользователя
    rental_payload_less_than_7_days["discount_policy"] = rental_discount.id  # Применяем скидку

    # Выводим запрос для отладки
    print(rental_payload_less_than_7_days)

    response = api_client.post("/api/v1/kashiring/rental/create/", rental_payload_less_than_7_days, format="json")

    # Выводим ошибку для отладки
    print(response.data)

    assert response.status_code == 201  # Проверяем успешное создание


@pytest.mark.django_db
def test_rental_price_with_discount_7_days(rental_payload_7_days, rental_discount, api_client, user):
    """Тест для аренды на 7 дней с применением скидки."""
    api_client.force_authenticate(user=user)  # Аутентификация пользователя
    
    # Добавляем поле user в тело запроса
    rental_payload_7_days["user"] = user.id  # Добавляем ID пользователя
    rental_payload_7_days["discount_policy"] = rental_discount.id  # Применяем скидку

    # Выводим запрос для отладки
    print(rental_payload_7_days)

    response = api_client.post("/api/v1/kashiring/rental/create/", rental_payload_7_days, format="json")

    # Выводим ошибку для отладки
    print(response.data)

    assert response.status_code == 201  # Проверяем успешное создание


@pytest.mark.django_db
def test_rental_price_with_discount_between_7_and_30_days(rental_payload_between_7_and_30_days, rental_discount, api_client, user):
    """Тест для аренды от 7 до 30 дней с применением скидки."""
    api_client.force_authenticate(user=user)  # Аутентификация пользователя
    
    # Добавляем поле user в тело запроса
    rental_payload_between_7_and_30_days["user"] = user.id  # Добавляем ID пользователя
    rental_payload_between_7_and_30_days["discount_policy"] = rental_discount.id  # Применяем скидку

    # Выводим запрос для отладки
    print(rental_payload_between_7_and_30_days)

    response = api_client.post("/api/v1/kashiring/rental/create/", rental_payload_between_7_and_30_days, format="json")

    # Выводим ошибку для отладки
    print(response.data)

    assert response.status_code == 201  # Проверяем успешное создание


@pytest.mark.django_db
def test_rental_price_with_discount_more_than_30_days(rental_payload_more_than_30_days, rental_discount, api_client, user):
    """Тест для аренды более 30 дней с применением скидки."""
    api_client.force_authenticate(user=user)  # Аутентификация пользователя
    
    # Добавляем поле user в тело запроса
    rental_payload_more_than_30_days["user"] = user.id  # Добавляем ID пользователя
    rental_payload_more_than_30_days["discount_policy"] = rental_discount.id  # Применяем скидку

    # Выводим запрос для отладки
    print(rental_payload_more_than_30_days)

    response = api_client.post("/api/v1/kashiring/rental/create/", rental_payload_more_than_30_days, format="json")

    # Выводим ошибку для отладки
    print(response.data)

    assert response.status_code == 201  # Проверяем успешное создание
