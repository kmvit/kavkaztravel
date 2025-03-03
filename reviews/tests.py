import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from reviews.models import Review, ReviewImage, Rating
from kashiring.models import Auto, Brand, Model, Year, Color, BodyType
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
def test_auto(db, test_user):
    """Создаём тестовый автомобиль"""
    brand = Brand.objects.create(name="Toyota")
    model = Model.objects.create(name="Camry")
    year = Year.objects.create(year=2020)
    color = Color.objects.create(name="Черный")
    body_type = BodyType.objects.create(name="Седан")

    return Auto.objects.create(
        brand=brand,
        model=model,
        year=year,
        color=color,
        body_type=body_type,
        owner=test_user,
    )


@pytest.fixture
def test_review(db, test_user, test_auto):
    review = Review.objects.create(
        user=test_user, car=test_auto, text="Тестовый отзыв", is_approved=True
    )
    review.save()
    return review


@pytest.fixture
def test_rating(db, test_review):
    rating = Rating.objects.create(review=test_review, criteria="cleanliness", score=5)
    rating.save()
    return rating


@pytest.fixture
def test_review_image(db, test_review):
    """Создаём тестовое изображение"""
    return ReviewImage.objects.create(review=test_review, image="test_image.jpg")


@pytest.fixture
def image_file():
    """Генерируем тестовое изображение"""
    image = BytesIO()
    img = Image.new("RGB", (100, 100), color="red")
    img.save(image, "JPEG")
    image.seek(0)
    return SimpleUploadedFile("test.jpg", image.read(), content_type="image/jpeg")


@pytest.mark.django_db
def test_create_review(auth_client, test_auto, test_user):
    """Тест создания отзыва с оценками"""

    data = {
        "user": test_user.id,
        "car": test_auto.id,
        "text": "Отличная машина!",
        "ratings": [{"criteria": "cleanliness", "score": 10}],
    }

    response = auth_client.post(BASE_URL, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Review.objects.count() == 1
    assert Review.objects.first().text == "Отличная машина!"
    assert Review.objects.first().ratings.count() == 1
    assert Review.objects.first().ratings.first().score == 10


@pytest.mark.django_db
def test_reviews_pagination(auth_client, test_auto, test_user):
    """Тест списка отзывов с проверкой структуры ответа и работы пагинации"""

    # Создаём 7 отзывов (чтобы проверить разбиение на страницы)
    reviews = [
        Review.objects.create(
            user=test_user, car=test_auto, text=f"Отзыв {i}", is_approved=True
        )
        for i in range(7)
    ]

    # Запрос первой страницы с 5 отзывами
    response = auth_client.get(f"{BASE_URL}?page_size=5")

    assert response.status_code == status.HTTP_200_OK

    # Проверяем структуру пагинационного ответа
    assert "count" in response.data  # Общее количество отзывов
    assert "next" in response.data  # Ссылка на следующую страницу (если есть)
    assert "previous" in response.data  # Ссылка на предыдущую страницу (если есть)
    assert "results" in response.data  # Список отзывов на текущей странице

    assert response.data["count"] == 7  # Всего 7 отзывов
    assert response.data["next"] is not None  # Должна быть следующая страница
    assert response.data["previous"] is None  # Первая страница, предыдущей нет

    # Проверяем, что на первой странице 5 отзывов
    assert len(response.data["results"]) == 5

    # Запрос второй страницы
    response_page_2 = auth_client.get(f"{BASE_URL}?page=2&page_size=5")

    assert response_page_2.status_code == status.HTTP_200_OK
    assert (
        response_page_2.data["previous"] is not None
    )  # Должна быть ссылка на первую страницу
    assert (
        response_page_2.data["next"] is None
    )  # Следующей страницы нет, так как всего 7 отзывов
    assert len(response_page_2.data["results"]) == 2  # Оставшиеся 2 отзыва


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
    assert Review.objects.count() == 0


@pytest.mark.django_db
def test_upload_image(auth_client, test_review, image_file):
    """Тест загрузки изображения к отзыву"""

    # Проверяем, что фикстура создала отзыв
    assert test_review is not None, "Фикстура test_review не создала отзыв"

    # Отправляем запрос на загрузку изображения
    response = auth_client.post(
        "/api/v1/reviews/car-images/",
        {"review_id": test_review.id, "image": image_file},
    )

    # Проверяем, что изображение загружено
    assert response.status_code == 201
    assert ReviewImage.objects.filter(review=test_review).exists()


@pytest.mark.django_db
def test_delete_image(auth_client, test_review_image):
    """Тест удаления изображения"""
    response = auth_client.delete(f"{IMAGE_URL}{test_review_image.id}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert ReviewImage.objects.count() == 0


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
    assert Review.objects.count() == 0  # Убедимся, что отзыв удалён


@pytest.mark.django_db
def test_full_review_flow(auth_client, test_auto, test_user, image_file):
    """Интеграционный тест: полный сценарий работы с отзывами"""

    # 1. Создание отзыва
    review_data = {
        "user": test_user.id,
        "car": test_auto.id,
        "text": "Отличная машина!",
        "ratings": [{"criteria": "cleanliness", "score": 10}],
    }

    create_response = auth_client.post(BASE_URL, review_data, format="json")
    review_id = create_response.data["id"]
    review = Review.objects.get(id=review_id)
    review.is_approved = True
    review.save()
    assert create_response.status_code == status.HTTP_201_CREATED

    assert Review.objects.filter(id=review_id).exists()

    # 2. Получение созданного отзыва
    get_response = auth_client.get(f"{BASE_URL}{review_id}/")

    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.data["text"] == "Отличная машина!"

    # 3. Добавление изображения к отзыву
    upload_response = auth_client.post(
        IMAGE_URL, {"review_id": review_id, "image": image_file}, format="multipart"
    )
    assert upload_response.status_code == status.HTTP_201_CREATED
    assert ReviewImage.objects.filter(review_id=review_id).exists()

    # 4. Обновление отзыва
    update_data = {"text": "Обновленный отзыв"}
    update_response = auth_client.patch(
        f"{BASE_URL}{review_id}/", update_data, format="json"
    )
    assert update_response.status_code == status.HTTP_200_OK
    assert Review.objects.get(id=review_id).text == "Обновленный отзыв"

    # 5. Удаление отзыва
    delete_response = auth_client.delete(f"{BASE_URL}{review_id}/")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT
    assert not Review.objects.filter(id=review_id).exists()

    # 6. Проверка удаления связанных данных
    assert not ReviewImage.objects.filter(review_id=review_id).exists()


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
def test_anonymous_user_cannot_create_review(api_client, test_auto):
    """Анонимный пользователь не может создавать отзывы"""

    review_data = {
        "car": test_auto.id,
        "text": "Хорошая машина!",
        "ratings": [{"criteria": "cleanliness", "score": 8}],
    }

    response = api_client.post(BASE_URL, review_data, format="json")

    assert (
        response.status_code == status.HTTP_401_UNAUTHORIZED
    ), "Анонимный пользователь смог создать отзыв"
