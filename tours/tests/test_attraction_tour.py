import pytest
from rest_framework import status

url = "http://127.0.0.1:8000/api/v1/tours/attractions/"


@pytest.mark.django_db
def test_create_attraction(api_client, parent_region):
    """
    Тест на создание достопримечательности через POST-запрос.

    Проверяет, что достопримечательность создаётся успешно и возвращаются корректные данные.
    """
    data = {
        "name": "Озеро Байкал",
        "description": "Самое глубокое озеро на планете",
        "region": parent_region.id
    }

    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "Озеро Байкал"
    assert response.data["region"] == parent_region.id


@pytest.mark.django_db
def test_list_attractions(api_client, attraction_tour):
    """
    Тест на получение списка достопримечательностей (GET-запрос на коллекцию).

    Проверяет, что вернулся список и в нём содержится нужный объект.
    """
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert any(item["name"] == "Эльбрус" for item in response.data)


@pytest.mark.django_db
def test_retrieve_attraction(api_client, attraction_tour):
    """
    Тест на получение конкретной достопримечательности по ID.

    Проверяет, что возвращаются корректные данные о достопримечательности.
    """
    detail_url = f"{url}{attraction_tour.id}/"
    response = api_client.get(detail_url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Эльбрус"


@pytest.mark.django_db
def test_update_attraction(api_client, attraction_tour, parent_region):
    """
    Тест на полное обновление данных достопримечательности (PUT-запрос).

    Проверяет, что данные обновляются корректно и возвращаются обновлённые значения.
    """
    detail_url = f"{url}{attraction_tour.id}/"
    updated_data = {
        "name": "Гора Эльбрус",
        "description": "Обновленное описание",
        "region": parent_region.id
    }
    response = api_client.put(detail_url, updated_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Гора Эльбрус"
    assert response.data["description"] == "Обновленное описание"


@pytest.mark.django_db
def test_partial_update_attraction(api_client, attraction_tour):
    """
    Тест на частичное обновление данных достопримечательности (PATCH-запрос).

    Проверяет, что можно изменить отдельное поле, не затрагивая остальные.
    """
    detail_url = f"{url}{attraction_tour.id}/"
    response = api_client.patch(detail_url, {"description": "Краткое обновление"})
    assert response.status_code == status.HTTP_200_OK
    assert response.data["description"] == "Краткое обновление"


@pytest.mark.django_db
def test_delete_attraction(api_client, attraction_tour):
    """
    Тест на удаление достопримечательности (DELETE-запрос).

    Проверяет, что после удаления объект недоступен и возвращается 404.
    """
    detail_url = f"{url}{attraction_tour.id}/"
    response = api_client.delete(detail_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Проверим, что объект действительно удалён
    get_response = api_client.get(detail_url)
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
def test_create_duplicate_name_attraction(api_client, parent_region):
    """
    Тест на уникальность названия достопримечательности.

    Проверяет, что при попытке создать достопримечательность с уже существующим названием,
    API возвращает ошибку 400.
    """
    data = {
        "name": "Озеро Байкал",
        "description": "Глубокое озеро",
        "region": parent_region.id
    }
    # Первый запрос проходит
    response1 = api_client.post(url, data)
    assert response1.status_code == status.HTTP_201_CREATED

    # Второй с тем же именем должен упасть
    response2 = api_client.post(url, data)
    assert response2.status_code == status.HTTP_400_BAD_REQUEST
    assert "name" in response2.data
