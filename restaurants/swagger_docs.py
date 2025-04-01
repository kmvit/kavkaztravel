from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from .serializers import (
    RestaurantDetailSerializer,
    RestaurantListSerializer,
    RestaurantImageSerializer,
    RestaurantSerializer,
)

# 📌 Restaurant Endpoints
restaurant_list = extend_schema(
    summary="📄 Список ресторанов",
    description="Получение списка всех ресторанов с основной информацией.",
    parameters=[
        OpenApiParameter(
            name="region",
            type=int,
            location=OpenApiParameter.QUERY,
            description="Фильтр по ID региона",
            required=False,
        ),
        OpenApiParameter(
            name="type",
            type=int,
            location=OpenApiParameter.QUERY,
            description="Фильтр по типу ресторана",
            required=False,
        ),
    ],
    responses={
        200: RestaurantListSerializer(many=True),
    },
)

restaurant_create = extend_schema(
    summary="➕ Создать ресторан",
    description="Создание нового ресторана. Требуются права владельца.",
    request=RestaurantDetailSerializer,
    responses={
        201: RestaurantSerializer,
        400: OpenApiResponse(description="Неверные данные"),
        403: OpenApiResponse(description="Доступ запрещен"),
    },
)

restaurant_detail = extend_schema(
    summary="🔍 Детали ресторана",
    description="Полная информация о конкретном ресторане.",
    responses={
        200: RestaurantDetailSerializer,
        404: OpenApiResponse(description="Ресторан не найден"),
    },
)

restaurant_update = extend_schema(
    summary="✏️ Обновить ресторан",
    description="Частичное обновление информации о ресторане. Только для владельца.",
    request=RestaurantSerializer,
    responses={
        200: RestaurantSerializer,
        400: OpenApiResponse(description="Неверные данные"),
        403: OpenApiResponse(description="Доступ запрещен"),
        404: OpenApiResponse(description="Ресторан не найден"),
    },
)

restaurant_delete = extend_schema(
    summary="🗑️ Удалить ресторан",
    description="Удаление ресторана. Только для владельца.",
    responses={
        204: OpenApiResponse(description="Ресторан удален"),
        403: OpenApiResponse(description="Доступ запрещен"),
        404: OpenApiResponse(description="Ресторан не найден"),
    },
)


restaurant_image_upload = extend_schema(
    summary="📤 Загрузить изображение ресторана",
    description="""
    Загрузка нового изображения для конкретного ресторана.
    Обязательные поля:
    - image: файл изображения
    - restaurant: ID ресторана
    """,
    request={
        "multipart/form-data": {
            "type": "object",
            "properties": {
                "image": {
                    "type": "string",
                    "format": "binary",
                    "description": "Файл изображения (JPEG/PNG/WEBP, макс. 5MB)",
                },
                "restaurant": {
                    "type": "integer",
                    "description": "ID ресторана, к которому прикрепляется изображение",
                },
            },
            "required": ["image", "restaurant"],
        }
    },
    responses={
        201: RestaurantImageSerializer,
        400: OpenApiResponse(
            description="Неверные данные: отсутствует restaurant или неверный формат изображения"
        ),
        403: OpenApiResponse(description="Доступ запрещен"),
        404: OpenApiResponse(description="Ресторан не найден"),
    },
)


restaurant_image_update = extend_schema(
    summary="🔄 Обновить изображение",
    description="Замена существующего изображения. Только для владельца.",
    request={
        "multipart/form-data": {
            "type": "object",
            "properties": {
                "image": {
                    "type": "string",
                    "format": "binary",
                    "description": "Новый файл изображения",
                }
            },
            "required": ["image"],
        }
    },
    responses={
        200: RestaurantImageSerializer,
        400: OpenApiResponse(description="Ошибка загрузки"),
        403: OpenApiResponse(description="Доступ запрещен"),
        404: OpenApiResponse(description="Изображение не найдено"),
    },
)
restaurant_image_update = extend_schema(
    summary="🔄 Обновить изображение ресторана",
    description="""
    Замена существующего изображения ресторана.
    Поддерживает обновление как через основной endpoint, так и через nested route.
    """,
    request={
        "multipart/form-data": {
            "type": "object",
            "properties": {
                "image": {
                    "type": "string",
                    "format": "binary",
                    "description": "Новый файл изображения (обязательно)",
                }
            },
            "required": ["image"],
        }
    },
    responses={
        200: RestaurantImageSerializer,
        400: OpenApiResponse(description="Ошибка валидации файла"),
        403: OpenApiResponse(description="Доступ запрещен"),
        404: OpenApiResponse(description="Изображение не найдено"),
    },
)

restaurant_image_delete = extend_schema(
    summary="🗑️ Удалить изображение ресторана",
    description="""
    Удаление изображения ресторана.
    Только для владельца ресторана.
    """,
    responses={
        204: OpenApiResponse(description="Изображение удалено"),
        403: OpenApiResponse(description="Доступ запрещен"),
        404: OpenApiResponse(description="Изображение не найдено"),
    },
)
