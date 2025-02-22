from drf_spectacular.utils import extend_schema
from .serializers import CarSerializer, CarImageSerializer, RentalConditionSerializer


class CarSwagger:
    """Документация для API автомобилей."""

    car_list = extend_schema(
        methods=["GET"],
        summary="📋 Список автомобилей",
        description="Возвращает список всех автомобилей.",
        responses={200: CarSerializer(many=True)}
    )

    car_create = extend_schema(
        methods=["POST"],
        summary="➕ Добавить автомобиль",
        description="Создаёт новый автомобиль.",
        request=CarSerializer,
        responses={201: CarSerializer, 400: "Ошибка"}
    )

    car_detail = extend_schema(
        methods=["GET"],
        summary="🔍 Детали автомобиля",
        description="Получает данные об автомобиле по ID.",
        responses={200: CarSerializer, 404: "Не найдено"}
    )

    car_update = extend_schema(
        methods=["PUT", "PATCH"],  # ✅ Добавили PATCH
        summary="✏️ Обновить автомобиль",
        description="Обновляет данные автомобиля. Можно использовать `PUT` или `PATCH`.",
        request=CarSerializer,
        responses={200: CarSerializer, 400: "Ошибка", 404: "Не найдено"}
    )

    car_delete = extend_schema(
        methods=["DELETE"],
        summary="🗑️ Удалить автомобиль",
        description="Удаляет автомобиль по ID.",
        responses={204: None, 404: "Не найдено"}
    )


class CarImageSwagger:
    """Документация для API изображений автомобилей."""

    image_list = extend_schema(
        methods=["GET"],
        summary="🖼️ Список изображений",
        description="Возвращает список всех изображений автомобилей.",
        responses={200: CarImageSerializer(many=True)}
    )

    image_create = extend_schema(
        methods=["POST"],
        summary="📷 Добавить изображение",
        description="Загружает новое изображение автомобиля.",
        request=CarImageSerializer,
        responses={201: CarImageSerializer, 400: "Ошибка"}
    )

    image_detail = extend_schema(
        methods=["GET"],
        summary="🔍 Детали изображения",
        description="Получает изображение автомобиля по ID.",
        responses={200: CarImageSerializer, 404: "Не найдено"}
    )

    image_delete = extend_schema(
        methods=["DELETE"],
        summary="❌ Удалить изображение",
        description="Удаляет изображение автомобиля по ID.",
        responses={204: None, 404: "Не найдено"}
    )


class RentalConditionSwagger:
    """Документация для API условий аренды."""

    rental_list = extend_schema(
        methods=["GET"],
        summary="📜 Список условий аренды",
        description="Возвращает список всех условий аренды.",
        responses={200: RentalConditionSerializer(many=True)}
    )

    rental_create = extend_schema(
        methods=["POST"],
        summary="📝 Добавить условия аренды",
        description="Создаёт новое условие аренды.",
        request=RentalConditionSerializer,
        responses={201: RentalConditionSerializer, 400: "Ошибка"}
    )

    rental_detail = extend_schema(
        methods=["GET"],
        summary="🔍 Детали условий аренды",
        description="Получает условия аренды по ID.",
        responses={200: RentalConditionSerializer, 404: "Не найдено"}
    )

    rental_update = extend_schema(
        methods=["PUT", "PATCH"],  # ✅ Добавили PATCH
        summary="✏️ Обновить условия аренды",
        description="Обновляет условия аренды. Можно использовать `PUT` или `PATCH`.",
        request=RentalConditionSerializer,
        responses={200: RentalConditionSerializer, 400: "Ошибка", 404: "Не найдено"}
    )
