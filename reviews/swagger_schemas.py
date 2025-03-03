from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from .serializers import (
    ReviewDetailSerializer,
    ReviewCreateUpdateSerializer,
    ReviewImageSerializer,
)

# 📌 Схемы для работы с отзывами
review_create = extend_schema(
    methods=["POST"],
    summary="➕ Добавить отзыв",
    description="Создаёт новый отзыв на автомобиль.",
    request=ReviewCreateUpdateSerializer,
    responses={
        201: ReviewDetailSerializer,
        400: OpenApiResponse(description="Ошибка валидации"),
    },
)

review_list = extend_schema(
    methods=["GET"],
    summary="📄 Список отзывов",
    description="Возвращает список всех одобренных отзывов.",
    responses={200: ReviewDetailSerializer(many=True)},
)

review_detail = extend_schema(
    methods=["GET"],
    summary="🔍 Просмотр отзыва",
    description="Возвращает детальную информацию об отзыве, включая оценки и изображения.",
    responses={
        200: ReviewDetailSerializer,
        404: OpenApiResponse(description="Отзыв не найден"),
    },
)

review_update = extend_schema(
    methods=["PATCH"],
    summary="✏️ Частичное обновление отзыва",
    description="Позволяет обновить текст отзыва или оценки.",
    request=ReviewCreateUpdateSerializer,
    responses={
        200: ReviewDetailSerializer,
        403: OpenApiResponse(description="Доступ запрещён"),
        404: OpenApiResponse(description="Отзыв не найден"),
    },
)

review_replace = extend_schema(
    methods=["PUT"],
    summary="🔄 Полное обновление отзыва",
    description="Заменяет весь отзыв новыми данными.",
    request=ReviewCreateUpdateSerializer,
    responses={
        200: ReviewDetailSerializer,
        400: OpenApiResponse(description="Ошибка валидации"),
        403: OpenApiResponse(description="Доступ запрещён"),
        404: OpenApiResponse(description="Отзыв не найден"),
    },
)

review_delete = extend_schema(
    methods=["DELETE"],
    summary="🗑️ Удалить отзыв",
    description="Удаляет отзыв. Только владелец или админ может удалить отзыв.",
    responses={
        204: OpenApiResponse(description="Отзыв удалён"),
        403: OpenApiResponse(description="Доступ запрещён"),
        404: OpenApiResponse(description="Отзыв не найден"),
    },
)

# 📌 Схемы для работы с изображениями
review_image_upload = extend_schema(
    methods=["POST"],
    summary="📤 Загрузить изображение",
    description="Позволяет загрузить изображение к отзыву.",
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
        201: ReviewImageSerializer,
        400: OpenApiResponse(description="Ошибка загрузки файла"),
        403: OpenApiResponse(description="Нет прав на загрузку"),
    },
)

review_image_list = extend_schema(
    methods=["GET"],
    summary="📷 Список изображений отзыва",
    description="Возвращает список всех изображений, прикреплённых к отзыву.",
    parameters=[
        OpenApiParameter(
            name="review",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description="ID отзыва для фильтрации изображений",
        )
    ],
    responses={200: ReviewImageSerializer(many=True)},
)

review_image_detail = extend_schema(
    methods=["GET"],
    summary="🔍 Просмотр изображения",
    description="Возвращает информацию об одном изображении отзыва.",
    responses={
        200: ReviewImageSerializer,
        404: OpenApiResponse(description="Изображение не найдено"),
    },
)

review_image_update = extend_schema(
    methods=["PUT"],
    summary="✏️ Обновить изображение",
    description="Позволяет заменить изображение в отзыве на новое.",
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
        200: ReviewImageSerializer,
        400: OpenApiResponse(description="Ошибка загрузки"),
        403: OpenApiResponse(description="Доступ запрещён"),
        404: OpenApiResponse(description="Изображение не найдено"),
    },
)

review_image_delete = extend_schema(
    methods=["DELETE"],
    summary="🗑️ Удалить изображение",
    description="Удаляет изображение, прикреплённое к отзыву.",
    responses={
        204: OpenApiResponse(description="Изображение удалено"),
        403: OpenApiResponse(description="Доступ запрещён"),
        404: OpenApiResponse(description="Изображение не найдено"),
    },
)
