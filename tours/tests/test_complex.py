import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
import random


# Генератор изображения (1x1 пиксель, валидный GIF)
def get_image_file():
    return SimpleUploadedFile(
        "test.gif",
        b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xFF\xFF\xFF\x21\xF9\x04"
        b"\x01\x0A\x00\x01\x00\x2C\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4C\x01\x00\x3B",
        content_type="image/gif",
    )


@pytest.mark.django_db
def test_full_tour_flow(api_client, user, region, tags):
    # 1. Создание 10 тэгов
    all_tags = []
    for i in range(10):
        response = api_client.post(
            "/api/v1/tours/tag/",
            {
                "name": f"Тег {i}",
                "description": f"Описание {i}",
                "tag_type": f"Тип {i}",
            },
        )
        assert response.status_code == 201
        all_tags.append(response.data["id"])

    # 2. Создание 20 туров
    tour_ids = []
    for i in range(20):
        response = api_client.post(
            "/api/v1/tours/current/",
            {
                "title": f"Тур {i}",
                "description": f"Описание тура {i}",
                "terms": f"Условия {i}",
                "region": region.id,
                "price": 1000 * (i + 1),
                "tags": random.sample(all_tags, k=random.randint(1, 3)),
            },
            format="json",
        )
        assert response.status_code == 201, f"Ошибка создания тура {i}: {response.data}"
        tour_ids.append(response.data["id"])

    # 3. Добавление изображений к каждому туру
    for tour_id in tour_ids:
        response = api_client.post(
            "/api/v1/tours/gallery_tour/",
            {"tour": tour_id, "image": get_image_file()},
            format="multipart",
        )
        assert (
            response.status_code == 201
        ), f"Не удалось загрузить картинку для тура {tour_id}: {response.data}"

    # 4. Проверка, что общее число туров = 20
    response = api_client.get("/api/v1/tours/current/")
    assert response.status_code == 200
    assert response.data["count"] == 20
    assert len(response.data["results"]) == 20
    # 5. Фильтрация по региону, цене и тэгу
    sample_tag = all_tags[0]
    response = api_client.get(
        f"/api/v1/tours/current/?region={region.id}&min_price=1000&max_price=20000&tags={sample_tag}"
    )
    assert response.status_code == 200
    assert response.data["count"] >= 0

    # 6. Получение детальной информации по одному туру
    sample_tour_id = tour_ids[0]
    response = api_client.get(f"/api/v1/tours/current/{sample_tour_id}/")
    assert response.status_code == 200
    assert "gallery_tour" in response.data
    assert "tags" in response.data

    # 7. Создание бронирования (от пользователя)
    api_client.force_authenticate(user=user)  # переключаемся на обычного пользователя
    response = api_client.post(
        "/api/v1/tours/order/",
        {
            "tour": sample_tour_id,
            "date": "2025-06-01",
            "size": 2,
            "username": "Тестовый клиент",
            "email": "client@test.com",
            "phone": "+71234567890",
        },
        format="json",
    )
    assert response.status_code == 201, f"Ошибка создания брони: {response.data}"
