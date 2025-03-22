import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.core.files.uploadedfile import InMemoryUploadedFile
from reviews.models import CarReview, CarReviewImage, CarRating
from kashiring.models import (
    Car,
    CarFeature,
    CarImage,
    RentalDiscount,
    RentalCondition,
    Brand,
    Model,
    CarOption,
    CarEquipment,
)
from io import BytesIO
from PIL import Image


BASE_URL = "/api/v1/reviews/car/"
IMAGE_URL = "/api/v1/reviews/car-images/"

User = get_user_model()


@pytest.fixture
def api_client():
    """Фикстура API клиента"""
    return APIClient()


@pytest.fixture
def auth_other_client(other_user):
    """Отдельный API клиент для другого пользователя"""
    client = APIClient()  # Создаём новый экземпляр APIClient
    client.force_authenticate(user=other_user)
    return client


@pytest.fixture
def test_user(db):
    """Создаём тестового пользователя"""
    return User.objects.create_user(
        username="testuser", email="testuser@example.com", password="testpass"
    )


@pytest.fixture
def other_user(db):
    """Создаёт второго пользователя (не владельца отзыва)"""
    return User.objects.create_user(
        username="otheruser", email="otheruser@example.com", password="testpass"
    )


@pytest.fixture
def auth_other_client(api_client, other_user):
    """Логиним второго пользователя"""
    api_client.force_authenticate(user=other_user)
    return api_client


@pytest.fixture
def auth_client(api_client, test_user):
    """Создаём отдельный API клиент для владельца отзыва"""
    client = APIClient()  # Создаём новый экземпляр
    client.force_authenticate(user=test_user)
    return client


@pytest.fixture
def third_user(db):
    """Создаёт третьего пользователя"""
    return User.objects.create_user(
        username="thirduser", email="thirduser@example.com", password="testpass"
    )


# Новый пользователь 2
@pytest.fixture
def fourth_user(db):
    """Создаёт четвертого пользователя"""
    return User.objects.create_user(
        username="fourthuser", email="fourthuser@example.com", password="testpass"
    )


# Фикстура для владельца машины
@pytest.fixture
def owner(db):
    """Фикстура для пользователя-владельца."""
    User = get_user_model()
    return User.objects.create_user(
        username="owner_user", password="password123", email="owner@example.com"
    )


# Фикстура для арендатора (не владельца)
@pytest.fixture
def user(db):
    """Фикстура для пользователя, не являющегося владельцем машины."""
    User = get_user_model()
    return User.objects.create_user(
        username="renter_user", password="password123", email="renter@example.com"
    )


@pytest.fixture
def rental_discount(db):
    """Фикстура для создания тестовой скидки (неделя + месяц)."""
    return RentalDiscount.objects.create(
        name="123", discount_week=5.00, discount_month=10.00
    )


@pytest.fixture
def brand_kia(db):
    return Brand.objects.create(name="Kia")


@pytest.fixture
def brand_toyota(db):
    return Brand.objects.create(name="Toyota")


@pytest.fixture
def model_rio(db):
    return Model.objects.create(name="Rio")


@pytest.fixture
def model_camry(
    db,
):
    return Model.objects.create(name="Camry")


@pytest.fixture
def car_option_1(car_1):
    """Фикстура для дополнительной опции автомобиля."""
    option = CarOption.objects.create(car=car_1, name="Leather Seats", price=500.00)
    return option


@pytest.fixture
def car_equipment_1(car_1):
    """Фикстура для комплектации автомобиля."""
    equipment = CarEquipment.objects.create(car=car_1, name="Premium Sound System")
    return equipment


@pytest.fixture
def car_1(db, owner, rental_discount, model_rio, brand_kia):
    """Фикстура для создания первого тестового автомобиля с заданным тарифом и моделью."""
    return Car.objects.create(
        owner=owner,
        brand=brand_kia,
        model=model_rio,
        description="Не совсем комфортый седан",
        body_type="sedan",
        year_of_production=2022,
        engine_power=123,
        drive_type="fwd",
        engine_type="petrol",
        price_per_day=100,
        discount_policy=rental_discount,
    )


@pytest.fixture
def car_2(db, owner, model_camry, brand_toyota):
    """Фикстура для создания второго тестового автомобиля без скидки."""
    return Car.objects.create(
        owner=owner,
        brand=brand_toyota,
        model=model_camry,
        description="Бизнес-седан",
        body_type="sedan",
        year_of_production=2021,
        engine_power=249,
        drive_type="fwd",
        engine_type="petrol",
        price_per_day=6100,
        discount_policy=None,
    )


@pytest.fixture
def test_review(db, test_user, car_1):
    car_review = CarReview.objects.create(
        user=test_user, car=car_1, text="Тестовый отзыв", is_approved=True, score=8
    )
    car_review.save()
    return car_review


@pytest.fixture
def test_rating(db, test_review):
    rating = CarRating.objects.create(
        car_review=test_review, criteria="cleanliness", score=5
    )
    rating.save()
    return rating


@pytest.fixture
def image_file_1():
    """Генерируем первое тестовое изображение"""
    image = BytesIO()
    img = Image.new("RGB", (100, 100), color="red")
    img.save(image, "JPEG")
    image.seek(0)
    return InMemoryUploadedFile(
        image, None, "image1.jpg", "image/jpeg", image.tell(), None
    )


@pytest.fixture
def image_file_2():
    """Генерируем второе тестовое изображение"""
    image = BytesIO()
    img = Image.new("RGB", (100, 100), color="green")
    img.save(image, "JPEG")
    image.seek(0)
    return InMemoryUploadedFile(
        image, None, "image2.jpg", "image/jpeg", image.tell(), None
    )


@pytest.fixture
def image_file_3():
    """Генерируем третье тестовое изображение"""
    image = BytesIO()
    img = Image.new("RGB", (100, 100), color="blue")
    img.save(image, "JPEG")
    image.seek(0)
    return InMemoryUploadedFile(
        image, None, "image3.jpg", "image/jpeg", image.tell(), None
    )


@pytest.fixture
def test_review_image_1(db, test_review, image_file_1):
    """Создаём тестовое изображение для отзыва"""
    return CarReviewImage.objects.create(car_review=test_review, image=image_file_1)


@pytest.fixture
def test_review_image_2(db, test_review, image_file_2):
    """Создаём второе тестовое изображение для отзыва"""
    return CarReviewImage.objects.create(car_review=test_review, image=image_file_2)


@pytest.fixture
def test_review_image_3(db, test_review, image_file_3):
    """Создаём третье тестовое изображение для отзыва"""
    return CarReviewImage.objects.create(car_review=test_review, image=image_file_3)


@pytest.mark.django_db
def test_reviews_pagination_with_avg_ratings(
    auth_client, car_1, car_2, test_user, other_user, third_user, fourth_user
):
    """Тест списка отзывов с проверкой структуры ответа, работы пагинации и среднего рейтинга/количества отзывов."""

    # 1. Создаем отзывы через API-запросы
    review_data_list = [
        {
            "user": test_user.id,
            "car": car_1.id,
            "text": "Отзыв 1",
            "score": 5,
            "ratings": [
                {"criteria": "cleanliness", "score": 10},
                {"criteria": "service", "score": 9},
                {"criteria": "location", "score": 8},
                {"criteria": "photo_match", "score": 7},
                {"criteria": "price_quality", "score": 6},
            ],
        },
        {
            "user": other_user.id,
            "car": car_1.id,
            "text": "Отзыв 2",
            "score": 3,
            "ratings": [
                {"criteria": "cleanliness", "score": 8},
                {"criteria": "service", "score": 7},
                {"criteria": "location", "score": 6},
                {"criteria": "photo_match", "score": 5},
                {"criteria": "price_quality", "score": 4},
            ],
        },
        {
            "user": third_user.id,
            "car": car_1.id,
            "text": "Отзыв 3",
            "score": 1,
            "ratings": [
                {"criteria": "cleanliness", "score": 6},
                {"criteria": "service", "score": 5},
                {"criteria": "location", "score": 4},
                {"criteria": "photo_match", "score": 3},
                {"criteria": "price_quality", "score": 2},
            ],
        },
        {
            "user": fourth_user.id,
            "car": car_1.id,
            "text": "Отзыв 4",
            "score": 3,
            "ratings": [
                {"criteria": "cleanliness", "score": 4},
                {"criteria": "service", "score": 3},
                {"criteria": "location", "score": 2},
                {"criteria": "photo_match", "score": 1},
                {"criteria": "price_quality", "score": 8},
            ],
        },
        # Добавим отзывы для второго автомобиля car_2
        {
            "user": test_user.id,
            "car": car_2.id,
            "text": "Отзыв 5 для car_2",
            "score": 4,
            "ratings": [
                {"criteria": "cleanliness", "score": 9},
                {"criteria": "service", "score": 8},
                {"criteria": "location", "score": 7},
                {"criteria": "photo_match", "score": 6},
                {"criteria": "price_quality", "score": 5},
            ],
        },
        {
            "user": other_user.id,
            "car": car_2.id,
            "text": "Отзыв 6 для car_2",
            "score": 2,
            "ratings": [
                {"criteria": "cleanliness", "score": 5},
                {"criteria": "service", "score": 6},
                {"criteria": "location", "score": 4},
                {"criteria": "photo_match", "score": 3},
                {"criteria": "price_quality", "score": 2},
            ],
        },
    ]

    # Отправляем POST-запросы на создание отзывов
    for review_data in review_data_list:
        response = auth_client.post(BASE_URL, data=review_data, format="json")
        assert (
            response.status_code == status.HTTP_201_CREATED
        ), f"Ошибка создания отзыва: {response.data}"

        # Одобряем отзыв после его создания
        review_id = response.data["id"]
        review = CarReview.objects.get(id=review_id)
        review.is_approved = True
        review.save()

    # 2. Проверяем пагинацию для car_1 (по 2 отзыва на страницу)
    response_page_1 = auth_client.get(f"{BASE_URL}reviews_car/?car_id={car_1.id}")
    assert response_page_1.status_code == status.HTTP_200_OK
    assert (
        len(response_page_1.data["results"]) == 4
    )  # Ожидаем 4 отзыва на первой странице для car_1

    # 3. Проверяем средний рейтинг и количество отзывов для car_1
    response_avg_car_1 = auth_client.get(f"{BASE_URL}reviews_car/?car_id={car_1.id}")
    assert response_avg_car_1.status_code == status.HTTP_200_OK
    data_car_1 = response_avg_car_1.json()

    assert data_car_1["review_count"] == 4  # 4 отзыва для car_1
    assert data_car_1["average_rating"] == (5 + 3 + 1 + 3) / 4  # Средняя оценка = 3.0

    # 4. Проверяем средние значения по критериям для car_1
    expected_criteria_ratings_car_1 = {
        "cleanliness_avg": (10 + 8 + 6 + 4) / 4,  # 7.0
        "service_avg": (9 + 7 + 5 + 3) / 4,  # 6.0
        "location_avg": (8 + 6 + 4 + 2) / 4,  # 5.0
        "photo_match_avg": (7 + 5 + 3 + 1) / 4,  # 4.0
        "price_quality_avg": (6 + 4 + 2 + 8) / 4,  # 5.0
    }

    # Проверяем средние значения по каждому критерию для car_1
    for criteria, expected_value in expected_criteria_ratings_car_1.items():
        assert (
            data_car_1["averages"][criteria] == expected_value
        ), f"Ошибка в расчете {criteria}"

    # 5. Проверяем пагинацию для car_2 (по 2 отзыва на страницу)
    response_page_2 = auth_client.get(f"{BASE_URL}reviews_car/?car_id={car_2.id}")
    assert response_page_2.status_code == status.HTTP_200_OK
    assert (
        len(response_page_2.data["results"]) == 2
    )  # Ожидаем 2 отзыва на первой странице для car_2

    # 6. Проверяем средний рейтинг и количество отзывов для car_2
    response_avg_car_2 = auth_client.get(f"{BASE_URL}reviews_car/?car_id={car_2.id}")
    assert response_avg_car_2.status_code == status.HTTP_200_OK
    data_car_2 = response_avg_car_2.json()

    assert data_car_2["review_count"] == 2  # 2 отзыва для car_2
    assert data_car_2["average_rating"] == (4 + 2) / 2  # Средняя оценка = 3.0

    # 7. Проверяем средние значения по критериям для car_2
    expected_criteria_ratings_car_2 = {
        "cleanliness_avg": (9 + 5) / 2,  # 7.0
        "service_avg": (8 + 6) / 2,  # 7.0
        "location_avg": (7 + 4) / 2,  # 5.5
        "photo_match_avg": (6 + 3) / 2,  # 4.5
        "price_quality_avg": (5 + 2) / 2,  # 3.5
    }

    # Проверяем средние значения по каждому критерию для car_2
    for criteria, expected_value in expected_criteria_ratings_car_2.items():
        assert (
            data_car_2["averages"][criteria] == expected_value
        ), f"Ошибка в расчете {criteria}"

    # 8. Проверяем структуру ответа для пагинации
    for review in data_car_1["results"]:
        assert "id" in review
        assert "user" in review
        assert "car" in review
        assert "text" in review
        assert "score" in review


@pytest.mark.django_db
def test_get_single_review(
    auth_client,
    test_review,
    test_rating,
    test_review_image_1,
    test_review_image_2,
    test_review_image_3,
):
    """Тест получения одного отзыва со всеми связанными данными (оценками и изображениями)"""

    # Делаем GET-запрос
    response = auth_client.get(f"{BASE_URL}{test_review.id}/")

    # Проверяем статус-код
    assert response.status_code == status.HTTP_200_OK

    # Преобразуем ответ в JSON
    data = response.json()

    # Проверяем, что отзыв содержит ожидаемые данные
    assert "id" in data
    assert (
        data["id"] == test_review.id
    )  # Проверяем, что id отзыва совпадает с ожидаемым

    assert "car" in data
    assert (
        data["car"] == test_review.car.id
    )  # Проверяем, что id автомобиля в отзыве совпадает с ожидаемым

    assert "user" in data
    assert (
        data["user"] == test_review.user.id
    )  # Проверяем, что id пользователя совпадает с ожидаемым

    assert "text" in data
    assert (
        data["text"] == test_review.text
    )  # Проверяем, что текст отзыва соответствует ожидаемому

    assert "is_approved" in data
    assert (
        data["is_approved"] == test_review.is_approved
    )  # Проверяем, что поле is_approved соответствует ожидаемому значению

    assert "score" in data
    assert (
        data["score"] == test_review.score
    )  # Проверяем, что оценка совпадает с ожидаемым значением

    # Проверяем, что в отзыве есть изображения
    assert "images" in data
    assert len(data["images"]) == 3  # Проверяем, что передано 3 изображения

    for image_data in data["images"]:
        image_url = image_data["image"]
        assert image_url.startswith(
            "http://testserver/media/car_review_images/"
        )  # Проверяем, что URL начинается с правильного пути
        assert image_url.endswith(
            ".jpg"
        )  # Проверяем, что URL заканчивается на .jpg (или .jpeg)


@pytest.mark.django_db
def test_update_review(auth_client, test_review):

    data = {"text": "Обновленный отзыв"}
    response = auth_client.patch(f"{BASE_URL}{test_review.id}/", data, format="json")

    assert response.status_code == status.HTTP_200_OK
    test_review.refresh_from_db()
    assert test_review.text == "Обновленный отзыв"


@pytest.mark.django_db
def test_delete_review(auth_client, test_review):
    """Тест удаления отзыва"""

    response = auth_client.delete(f"{BASE_URL}{test_review.id}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert CarReview.objects.count() == 0


def test_upload_image(auth_client, test_review, image_file_1):
    """Тест загрузки одного изображения к отзыву"""

    # Проверяем, что фикстура создала отзыв
    assert test_review is not None, "Фикстура test_review не создала отзыв"

    # Отправляем запрос на загрузку одного изображения
    response = auth_client.post(
        "/api/v1/reviews/car-images/",
        {"car_review": test_review.id, "image": image_file_1},
        format="multipart",  # Указываем формат для загрузки файлов
    )

    # Проверяем, что статус ответа успешный
    assert response.status_code == 201, f"Ошибка: {response.data}"

    # Отправляем запрос на получение всех изображений для отзыва
    response_get = auth_client.get(
        f"/api/v1/reviews/car-images/",
    )

    # Проверяем, что статус ответа успешный
    assert (
        response_get.status_code == 200
    ), f"Ошибка при получении изображений: {response_get.data}"

    # Проверяем, что одно изображение было загружено
    assert (
        len(response_get.data) == 1
    ), f"Не все изображения были получены, получено: {len(response_get.data)}"


@pytest.mark.django_db
def test_delete_image(auth_client, test_review_image_1):
    """Тест удаления изображения"""
    response = auth_client.delete(f"{IMAGE_URL}{test_review_image_1.id}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert CarReviewImage.objects.count() == 0


@pytest.mark.django_db
def test_review_permissions(auth_client, auth_other_client, test_review):
    """Проверяем, что только владелец может редактировать/удалять отзыв"""

    update_data = {"text": "Попытка изменить чужой отзыв"}

    # Попытка редактировать отзыв чужим пользователем
    response = auth_other_client.patch(
        f"{BASE_URL}{test_review.id}/", update_data, format="json"
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN  # Доступ запрещён

    # Попытка удалить отзыв чужим пользователем
    response = auth_other_client.delete(f"{BASE_URL}{test_review.id}/")
    assert response.status_code == status.HTTP_403_FORBIDDEN  # Доступ запрещён

    # Владелец отзыва успешно обновляет его
    response = auth_client.patch(
        f"{BASE_URL}{test_review.id}/", update_data, format="json"
    )
    assert response.status_code == status.HTTP_200_OK
    test_review.refresh_from_db()
    assert test_review.text == "Попытка изменить чужой отзыв"

    # Владелец успешно удаляет отзыв
    response = auth_client.delete(f"{BASE_URL}{test_review.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert CarReview.objects.count() == 0  # Убедимся, что отзыв удалён


@pytest.mark.django_db
def test_full_review_flow(auth_client, car_1, test_user, image_file_1):
    """Интеграционный тест: полный сценарий работы с отзывами"""

    # 1. Создание отзыва
    review_data = {
        "user": test_user.id,
        "car": car_1.id,
        "text": "Отличная машина!",
        "score": 5,
        "ratings": [{"criteria": "cleanliness", "score": 10}],
    }

    create_response = auth_client.post(BASE_URL, review_data, format="json")
    review_id = create_response.data["id"]
    review = CarReview.objects.get(id=review_id)
    review.is_approved = True
    review.save()
    assert create_response.status_code == status.HTTP_201_CREATED

    assert CarReview.objects.filter(id=review_id).exists()

    # 2. Получение созданного отзыва
    get_response = auth_client.get(f"{BASE_URL}{review_id}/")

    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.data["text"] == "Отличная машина!"

    # 3. Добавление изображения к отзыву
    upload_response = auth_client.post(
        IMAGE_URL, {"car_review": review_id, "image": image_file_1}, format="multipart"
    )
    assert upload_response.status_code == status.HTTP_201_CREATED
    assert CarReviewImage.objects.filter(car_review=review_id).exists()

    # 4. Обновление отзыва
    update_data = {"text": "Обновленный отзыв"}
    update_response = auth_client.patch(
        f"{BASE_URL}{review_id}/", update_data, format="json"
    )
    assert update_response.status_code == status.HTTP_200_OK
    assert CarReview.objects.get(id=review_id).text == "Обновленный отзыв"

    # 5. Удаление отзыва
    delete_response = auth_client.delete(f"{BASE_URL}{review_id}/")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT
    assert not CarReview.objects.filter(id=review_id).exists()

    # 6. Проверка удаления связанных данных
    assert not CarReviewImage.objects.filter(car_review=review_id).exists()


@pytest.mark.django_db
def test_anonymous_user_can_view_reviews(api_client, test_review):
    """Анонимный пользователь должен иметь доступ к просмотру отзывов"""
    response = api_client.get(f"{BASE_URL}reviews_car/?car_id={test_review.car_id}")
    assert (
        response.status_code == status.HTTP_200_OK
    ), "Анонимный пользователь не может просматривать отзывы"
    response_data = response.json()
    assert "results" in response_data, f"Неверный формат ответа: {response_data}"
    assert test_review.id in [
        r["id"] for r in response_data["results"]
    ], "Отзыв отсутствует в списке"


@pytest.mark.django_db
def test_anonymous_user_cannot_create_review(api_client, car_1):
    """Анонимный пользователь не может создавать отзывы"""

    review_data = {
        "car": car_1.id,
        "text": "Хорошая машина!",
        "ratings": [{"criteria": "cleanliness", "score": 8}],
    }

    response = api_client.post(BASE_URL, review_data, format="json")

    assert (
        response.status_code == status.HTTP_401_UNAUTHORIZED
    ), "Анонимный пользователь смог создать отзыв"


@pytest.mark.django_db
def test_user_can_only_leave_one_review_for_car(auth_client, test_user, car_1):
    """Проверяем, что пользователь может оставить только один отзыв на одну машину."""

    # Создаем первый отзыв
    CarReview.objects.create(
        user=test_user,
        car=car_1,
        text="Отличная машина!",
        score=8,
        is_approved=True,
    )

    # Попытка создать второй отзыв для той же машины этим же пользователем
    response = auth_client.post(
        f"{BASE_URL}",
        {
            "user": test_user.id,
            "car": car_1.id,
            "text": "Еще один отзыв",
            "ratings": [{"criteria": "cleanliness", "score": 8}],
            "score": 7,
        },
        format="json",
    )

    # Проверяем, что второй отзыв не был добавлен
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "non_field_errors" in response.data
    assert (
        response.data["non_field_errors"][0]
        == "The fields user, car must make a unique set."
    )
