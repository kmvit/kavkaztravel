import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
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
def model_rio(db, brand_kia):
    return Model.objects.create(name="Rio")


@pytest.fixture
def model_camry(db, brand_toyota):
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
def car_1_features(db, car_1):
    """Фикстура для характеристик первого автомобиля."""
    return [
        CarFeature.objects.create(car=car_1, name="air_conditioning"),
        CarFeature.objects.create(car=car_1, name="four_doors"),
    ]


@pytest.fixture
def car_2_features(db, car_2):
    """Фикстура для характеристики второго автомобиля."""
    return [
        CarFeature.objects.create(car=car_2, name="air_conditioning"),
    ]


@pytest.fixture
def car_1_images(db, car_1):
    """Фикстура для изображений первого автомобиля."""
    return [
        CarImage.objects.create(car=car_1, image="car_images/endpoint.png"),
        CarImage.objects.create(car=car_1, image="car_images/db.png"),
    ]


@pytest.fixture
def car_2_images(db, car_2):
    """Фикстура для изображений второго автомобиля (пустой список)."""
    return []


@pytest.fixture
def test_review(db, test_user, car_1):
    car_review = CarReview.objects.create(
        user=test_user, car=car_1, text="Тестовый отзыв", is_approved=True, score=8
    )
    car_review.save()
    return  car_review


@pytest.fixture
def test_rating(db, test_review):
    rating = CarRating.objects.create(car_review=test_review, criteria="cleanliness", score=5)
    rating.save()
    return rating


@pytest.fixture
def test_review_image(db, test_review):
    """Создаём тестовое изображение"""
    return CarReviewImage.objects.create(car_review=test_review, image="test_image.jpg")


@pytest.fixture
def image_file():
    """Генерируем тестовое изображение"""
    image = BytesIO()
    img = Image.new("RGB", (100, 100), color="red")
    img.save(image, "JPEG")
    image.seek(0)
    return SimpleUploadedFile("test.jpg", image.read(), content_type="image/jpeg")


@pytest.mark.django_db
def test_create_review(auth_client, car_1, test_user):
    """Тест создания отзыва с оценками"""

    data = {
        "user": test_user.id,
        "car": car_1.id,
        "text": "Отличная машина!",
        "score": 5,
        "ratings": [{"criteria": "cleanliness", "score": 10}],
    }

    response = auth_client.post(BASE_URL, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert CarReview.objects.count() == 1
    assert CarReview.objects.first().text == "Отличная машина!"
    assert CarReview.objects.first().ratings.count() == 1
    assert CarReview.objects.first().ratings.first().score == 10


@pytest.mark.django_db
def test_reviews_pagination(auth_client, car_1, car_2, test_user, other_user, third_user, fourth_user):
    """Тест списка отзывов с проверкой структуры ответа, работы пагинации и среднего рейтинга/количества отзывов."""

    # 1. Для test_user создаем 3 отзыва для car_1
    CarReview.objects.create(
        user=test_user,
        car=car_1,
        text="Отзыв 1 от test_user для car_1",
        is_approved=True,
        score=5,
    )
    CarReview.objects.create(
        user=test_user,
        car=car_2,
        text="Отзыв 2 от test_user для car_1",
        is_approved=True,
        score=4,
    )
    CarReview.objects.create(
        user=other_user,
        car=car_1,
        text="Отзыв 3 от test_user для car_1",
        is_approved=True,
        score=3,
    )

    # 2. Для other_user создаем 2 отзыва для car_1
    CarReview.objects.create(
        user=other_user,
        car=car_2,
        text="Отзыв 1 от other_user для car_1",
        is_approved=True,
        score=2,
    )
    CarReview.objects.create(
        user=third_user,
        car=car_1,
        text="Отзыв 2 от other_user для car_1",
        is_approved=True,
        score=1,
    )

    # 3. Для third_user создаем 4 отзыва для car_2
    CarReview.objects.create(
        user=third_user,
        car=car_2,
        text="Отзыв 1 от third_user для car_2",
        is_approved=True,
        score=5,
    )
    CarReview.objects.create(
        user=fourth_user,
        car=car_1,
        text="Отзыв 3 от third_user для car_2",
        is_approved=True,
        score=3,
    )
    

    # Запрос на первую страницу (по умолчанию 5 записей на странице)
    response = auth_client.get(f"{BASE_URL}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 5  # Проверяем, что на первой странице 5 отзывов

    # Запрос на вторую страницу (остальные 3 отзыва)
    response_page_2 = auth_client.get(f"{BASE_URL}?page=2")
    assert response_page_2.status_code == status.HTTP_200_OK
    assert len(response_page_2.data["results"]) == 2  # На второй странице должно быть 3 отзыва

    # Проверка среднего рейтинга и количества отзывов для car_1
    car_1_review_count = CarReview.get_review_count(car_1)
    car_1_average_rating = CarReview.get_average_rating(car_1)
    
    assert car_1_review_count == 4  # Должно быть 5 одобренных отзывов для car_1
    assert car_1_average_rating == (5 + 3 + 1+3) / 4  

    # Проверка среднего рейтинга и количества отзывов для car_2
    car_2_review_count = CarReview.get_review_count(car_2)
    car_2_average_rating = CarReview.get_average_rating(car_2)

    assert car_2_review_count == 3  # Должно быть 5 одобренных отзывов для car_2
    assert car_2_average_rating == (4 + 2 + 5) / 3 


@pytest.mark.django_db
def test_get_single_review(auth_client, test_review, test_rating, test_review_image):
    """Тест получения одного отзыва со всеми связанными данными (оценками и изображениями)"""

    # Делаем GET-запрос
    response = auth_client.get(f"{BASE_URL}{test_review.id}/")
    # Проверяем статус-код
    assert response.status_code == status.HTTP_200_OK

    # Преобразуем ответ в JSON
    data = response.json()

    # Проверяем, что отзыв содержит ожидаемые данные
    assert data["is_approved"] is True
    assert "ratings" in data
    assert len(data["ratings"]) == 1
    assert data["ratings"][0]["id"] == test_rating.id
    assert data["ratings"][0]["criteria"] == test_rating.criteria
    assert data["ratings"][0]["score"] == test_rating.score

    # Проверяем, что в отзыве есть изображения
    assert "images" in data
    assert len(data["images"]) == 1

    # Проверяем, что путь к изображению корректный
    expected_image_url = f"http://testserver{test_review_image.image.url}"
    assert data["images"][0]["image"] == expected_image_url


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


@pytest.mark.django_db
def test_upload_image(auth_client, test_review, image_file):
    """Тест загрузки изображения к отзыву"""

    # Проверяем, что фикстура создала отзыв
    assert test_review is not None, "Фикстура test_review не создала отзыв"

    # Отправляем запрос на загрузку изображения
    response = auth_client.post(
        "/api/v1/reviews/car-images/",
        {"car_review": test_review.id, "image": image_file},  # Используем "car_review" вместо "car_review_id"
        format="multipart",  # Указываем формат для загрузки файла
    )

    # Проверяем, что изображение загружено
    assert response.status_code == 201, f"Ожидался статус 201, но получен {response.status_code}. Ответ: {response.data}"
    assert CarReviewImage.objects.filter(car_review=test_review).exists()


@pytest.mark.django_db
def test_delete_image(auth_client, test_review_image):
    """Тест удаления изображения"""
    response = auth_client.delete(f"{IMAGE_URL}{test_review_image.id}/")

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
def test_full_review_flow(auth_client, car_1, test_user, image_file):
    """Интеграционный тест: полный сценарий работы с отзывами"""

    # 1. Создание отзыва
    review_data = {
        "user": test_user.id,  # Здесь все равно передается id, так как это ID пользователя
        "car": car_1.id,  # ID автомобиля тоже передается, так как это FK
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
        IMAGE_URL, {"car_review": review_id, "image": image_file}, format="multipart"
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
    assert not CarReviewImage.objects.filter(car_review =review_id).exists()


@pytest.mark.django_db
def test_anonymous_user_can_view_reviews(api_client, test_review):
    """Анонимный пользователь должен иметь доступ к просмотру отзывов"""

    response = api_client.get(BASE_URL)

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
    response = auth_client.post(f"{BASE_URL}",
       
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
    assert response.data["non_field_errors"][0] == "The fields user, car must make a unique set."
