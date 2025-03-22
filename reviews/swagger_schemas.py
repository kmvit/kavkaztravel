from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from .serializers import (
    CarReviewDetailSerializer,  # Добавлен префикс Car
    CarReviewCreateUpdateSerializer,  # Добавлен префикс Car
    CarReviewImageSerializer,  # Добавлен префикс Car
)

# 📌 Схемы для работы с отзывами, привязанные к автомобилям
car_review_create = extend_schema(
    methods=["POST"],
    summary="➕ Добавить отзыв о машине",
    description="Создаёт новый отзыв на автомобиль.",
    request=CarReviewCreateUpdateSerializer,  # Использован префикс Car
    responses={
        201: CarReviewDetailSerializer,  # Использован префикс Car
        400: OpenApiResponse(description="Ошибка валидации"),
    },
)

car_review_car = extend_schema(
    methods=["GET"],
    summary="📄 Список отзывов о машине",
    description="Возвращает список всех одобренных отзывов о машине.",
    responses={200: CarReviewDetailSerializer(many=True)},  # Использован префикс Car
    parameters=[
        OpenApiParameter(
            name="car_id",
            type=int,
            location=OpenApiParameter.QUERY,  # Указываем, что это параметр в query
            description="ID машины, для которой нужно получить отзывы",
            required=True,  # Указываем, что параметр обязательный
        )
    ],
)

car_review_detail = extend_schema(
    methods=["GET"],
    summary="🔍 Просмотр отзыва о машине",
    description="Возвращает детальную информацию об отзыве на автомобиль, включая оценки и изображения.",
    responses={
        200: CarReviewDetailSerializer,  # Использован префикс Car
        404: OpenApiResponse(description="Отзыв не найден"),
    },
)

car_review_update = extend_schema(
    methods=["PATCH"],
    summary="✏️ Частичное обновление отзыва о машине",
    description="Позволяет обновить текст отзыва или оценки автомобиля.",
    request=CarReviewCreateUpdateSerializer,  # Использован префикс Car
    responses={
        200: CarReviewDetailSerializer,  # Использован префикс Car
        403: OpenApiResponse(description="Доступ запрещён"),
        404: OpenApiResponse(description="Отзыв не найден"),
    },
)

car_review_replace = extend_schema(
    methods=["PUT"],
    summary="🔄 Полное обновление отзыва о машине",
    description="Заменяет весь отзыв о машине новыми данными.",
    request=CarReviewCreateUpdateSerializer,  # Использован префикс Car
    responses={
        200: CarReviewDetailSerializer,  # Использован префикс Car
        400: OpenApiResponse(description="Ошибка валидации"),
        403: OpenApiResponse(description="Доступ запрещён"),
        404: OpenApiResponse(description="Отзыв не найден"),
    },
)

car_review_delete = extend_schema(
    methods=["DELETE"],
    summary="🗑️ Удалить отзыв о машине",
    description="Удаляет отзыв о машине. Только владелец или админ может удалить отзыв.",
    responses={
        204: OpenApiResponse(description="Отзыв удалён"),
        403: OpenApiResponse(description="Доступ запрещён"),
        404: OpenApiResponse(description="Отзыв не найден"),
    },
)

# 📌 Схемы для работы с изображениями отзыва о машине
car_review_image_upload = extend_schema(
    methods=["POST"],
    summary="📤 Загрузить изображение отзыва о машине",
    description="Позволяет загрузить изображение к отзыву о машине.",
    request={
        "multipart/form-data": {
            "type": "object",
            "properties": {
                "review": {"type": "integer", "example": 1},
                "image": {"type": "string", "format": "binary"},
            },
            "required": ["review", "image"],
        }
    },
    responses={
        201: CarReviewImageSerializer,  # Использован префикс Car
        400: OpenApiResponse(description="Ошибка загрузки файла"),
        403: OpenApiResponse(description="Нет прав на загрузку"),
    },
)

car_review_image_list = extend_schema(
    methods=["GET"],
    summary="📷 Список изображений отзыва о машине",
    description="Возвращает список всех изображений, прикреплённых к отзыву о машине.",
    parameters=[
        OpenApiParameter(
            name="review",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description="ID отзыва о машине для фильтрации изображений",
        )
    ],
    responses={200: CarReviewImageSerializer(many=True)},  # Использован префикс Car
)

car_review_image_detail = extend_schema(
    methods=["GET"],
    summary="🔍 Просмотр изображения отзыва о машине",
    description="Возвращает информацию об одном изображении отзыва о машине.",
    responses={
        200: CarReviewImageSerializer,  # Использован префикс Car
        404: OpenApiResponse(description="Изображение не найдено"),
    },
)

car_review_image_update = extend_schema(
    methods=["PUT"],
    summary="✏️ Обновить изображение отзыва о машине",
    description="Позволяет заменить изображение в отзыве о машине на новое.",
    request={
        "multipart/form-data": {
            "type": "object",
            "properties": {
                "image": {"type": "string", "format": "binary"},
            },
            "required": ["image"],
        }
    },
    responses={
        200: CarReviewImageSerializer,  # Использован префикс Car
        400: OpenApiResponse(description="Ошибка загрузки"),
        403: OpenApiResponse(description="Доступ запрещён"),
        404: OpenApiResponse(description="Изображение не найдено"),
    },
)

car_review_image_delete = extend_schema(
    methods=["DELETE"],
    summary="🗑️ Удалить изображение отзыва о машине",
    description="Удаляет изображение, прикреплённое к отзыву о машине.",
    responses={
        204: OpenApiResponse(description="Изображение удалено"),
        403: OpenApiResponse(description="Доступ запрещён"),
        404: OpenApiResponse(description="Изображение не найдено"),
    },
)
