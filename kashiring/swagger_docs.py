from drf_spectacular.utils import extend_schema
from .serializers import CarSerializer, CarImageSerializer, RentalConditionSerializer, CarCreateUpdateSerializer


class CarSwagger:
    """Документация для API автомобилей."""

    car_list = extend_schema(
        methods=["GET"],
        summary="📋 Список автомобилей",
        description="Возвращает список всех автомобилей.",
        responses={200: CarSerializer(many=True)}
    )

    # Схема для создания нового автомобиля
    car_create = extend_schema(
        methods=["POST"],
        summary="➕ Добавить автомобиль",  # Краткое описание
        description="Создаёт новый автомобиль.",  # Подробное описание
        request=CarCreateUpdateSerializer,  # Сериализатор для тела запроса
        responses={  # Ожидаемые ответы
            201: CarCreateUpdateSerializer,  # Успешный ответ с объектом автомобиля
            400: "Ошибка",  # Ответ в случае ошибки
        }
    )

    car_detail = extend_schema(
        methods=["GET"],
        summary="🔍 Детали автомобиля",
        description="Получает данные об автомобиле по ID.",
        responses={200: CarSerializer, 404: "Не найдено"}
    )

    # Схема для обновления или частичного обновления автомобиля
    car_update = extend_schema(
        methods=["PUT", "PATCH"],  # Поддержка PUT и PATCH
        summary="✏️ Обновить автомобиль",  # Краткое описание
        description="Обновляет данные автомобиля. Можно использовать `PUT` или `PATCH`.",  # Подробное описание
        request=CarCreateUpdateSerializer,  # Сериализатор для тела запроса
        responses={  # Ожидаемые ответы
            200: CarCreateUpdateSerializer,  # Успешный ответ с обновленными данными
            400: "Ошибка",  # Ошибка в запросе
            404: "Не найдено",  # Если объект не найден
        }
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

from drf_spectacular.utils import extend_schema
from .serializers import RentalDiscountSerializer, RentalSerializer

class RentalDiscountSwagger:
    """Документация для API тарифных планов (скидок на аренду)."""

    discount_list = extend_schema(
        methods=["GET"],
        summary="📜 Список тарифных планов",
        description="Возвращает список всех тарифных планов (скидок).",
        responses={200: RentalDiscountSerializer(many=True)}
    )

    discount_create = extend_schema(
        methods=["POST"],
        summary="📝 Добавить тарифный план",
        description="Создаёт новый тарифный план (скидку).",
        request=RentalDiscountSerializer,
        responses={201: RentalDiscountSerializer, 400: "Ошибка"}
    )

    discount_detail = extend_schema(
        methods=["GET"],
        summary="🔍 Детали тарифного плана",
        description="Получает тарифный план по ID.",
        responses={200: RentalDiscountSerializer, 404: "Не найдено"}
    )

    discount_update = extend_schema(
        methods=["PUT", "PATCH"],
        summary="✏️ Обновить тарифный план",
        description="Обновляет тарифный план. Можно использовать `PUT` или `PATCH`.",
        request=RentalDiscountSerializer,
        responses={200: RentalDiscountSerializer, 400: "Ошибка", 404: "Не найдено"}
    )

class RentalSwagger:
    """Документация для API аренды."""

    rental_create = extend_schema(
            methods=["POST"],
            summary="Создание аренды и возвращает общую стоимость аренды.",
            description="Создаёт новую аренду и возвращает общую стоимость аренды.",
            request=RentalSerializer(),  # ✅ Исправлено: передаём экземпляр
            responses={201: RentalSerializer(), 400: "Ошибка"}
        )
