import pytest
from rest_framework import status


import pytest
from rest_framework import status

@pytest.mark.django_db
def test_create_car_option(api_client, user, car_1):
    """Тест создания дополнительной опции автомобиля."""
    api_client.force_authenticate(user=user)
    print(car_1.id, 125)
    payload = {"car": car_1.id, "name": "Sunroof", "price": 2000.00}
    
    # Отладочный вывод
    print(f"Payload for creating car option: {payload}")
    print(f"Car ID used: {car_1.id}")

    response = api_client.post("/api/v1/kashiring/car-options/", payload, format="json")

    # Отладочный вывод
    print(f"Response status code: {response.status_code}")
    print(f"Response data: {response.data}")

    # Проверка статуса ответа
    assert response.status_code == status.HTTP_201_CREATED, f"Ошибка: {response.data}"
    assert response.data["name"] == "Sunroof", f"Expected 'Sunroof', but got {response.data['name']}"
    assert float(response.data["price"]) == 2000.00, f"Expected price 2000.00, but got {response.data['price']}"



@pytest.mark.django_db
def test_list_car_options(api_client, user, car_option_1):
    """Тест получения списка дополнительных опций автомобиля."""
    api_client.force_authenticate(user=user)

    response = api_client.get("/api/v1/kashiring/car-options/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0
    assert any(option["name"] == "Leather Seats" for option in response.data)


@pytest.mark.django_db
def test_retrieve_car_option(api_client, user, car_option_1):
    """Тест получения конкретной опции автомобиля по ID."""
    api_client.force_authenticate(user=user)

    response = api_client.get(f"/api/v1/kashiring/car-options/{car_option_1.id}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Leather Seats"


@pytest.mark.django_db
def test_update_car_option(api_client, user, car_option_1):
    """Тест обновления дополнительной опции автомобиля."""
    api_client.force_authenticate(user=user)

    updated_data = {"name": "Heated Seats", "price": 2500.00}
    response = api_client.patch(f"/api/v1/kashiring/car-options/{car_option_1.id}/", updated_data, format="json")

    assert response.status_code == status.HTTP_200_OK, f"Ошибка: {response.data}"
    assert response.data["name"] == "Heated Seats"
    assert float(response.data["price"]) == 2500.00


@pytest.mark.django_db
def test_delete_car_option(api_client, user, car_option_1):
    """Тест удаления дополнительной опции автомобиля."""
    api_client.force_authenticate(user=user)

    response = api_client.delete(f"/api/v1/kashiring/car-options/{car_option_1.id}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Проверяем, что объект действительно удалён
    response_check = api_client.get(f"/api/v1/kashiring/car-options/{car_option_1.id}/")
    assert response_check.status_code == status.HTTP_404_NOT_FOUND


# ---------------------- Тесты для CarEquipment ----------------------

@pytest.mark.django_db
def test_create_car_equipment(api_client, user, car_1):
    """Тест создания комплектации автомобиля."""
    api_client.force_authenticate(user=user)

    payload = {"car": car_1.id, "name": "Premium Sound System"}
    response = api_client.post("/api/v1/kashiring/car-equipment/", payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED, f"Ошибка: {response.data}"
    assert response.data["name"] == "Premium Sound System"


@pytest.mark.django_db
def test_list_car_equipment(api_client, user, car_equipment_1):
    """Тест получения списка комплектаций автомобиля."""
    api_client.force_authenticate(user=user)

    response = api_client.get("/api/v1/kashiring/car-equipment/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0
    assert any(equipment["name"] == "Premium Sound System" for equipment in response.data)


@pytest.mark.django_db
def test_retrieve_car_equipment(api_client, user, car_equipment_1):
    """Тест получения конкретной комплектации автомобиля по ID."""
    api_client.force_authenticate(user=user)

    response = api_client.get(f"/api/v1/kashiring/car-equipment/{car_equipment_1.id}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Premium Sound System"


@pytest.mark.django_db
def test_update_car_equipment(api_client, user, car_equipment_1):
    """Тест обновления комплектации автомобиля."""
    api_client.force_authenticate(user=user)

    updated_data = {"name": "Advanced Audio System"}
    response = api_client.patch(f"/api/v1/kashiring/car-equipment/{car_equipment_1.id}/", updated_data, format="json")

    assert response.status_code == status.HTTP_200_OK, f"Ошибка: {response.data}"
    assert response.data["name"] == "Advanced Audio System"


@pytest.mark.django_db
def test_delete_car_equipment(api_client, user, car_equipment_1):
    """Тест удаления комплектации автомобиля."""
    api_client.force_authenticate(user=user)

    response = api_client.delete(f"/api/v1/kashiring/car-equipment/{car_equipment_1.id}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Проверяем, что объект действительно удалён
    response_check = api_client.get(f"/api/v1/kashiring/car-equipment/{car_equipment_1.id}/")
    assert response_check.status_code == status.HTTP_404_NOT_FOUND
